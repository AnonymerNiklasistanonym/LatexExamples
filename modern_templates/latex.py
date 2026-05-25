#!/usr/bin/env python3

# Standard library
import argparse
import logging
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Iterable, List, Optional
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib.util
from dataclasses import dataclass, field


logger = logging.getLogger("latex")
logger_format = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M"
)
logger.setLevel(logging.DEBUG)

ROOT_DIR = Path(__file__).parent
DIST_DIR = ROOT_DIR / "build"
LATEX_INDENT_DIR = ROOT_DIR / "latex" / "latexindent"
LATEX_ASPELL_DIR = ROOT_DIR / "latex" / "aspell"

REQUIRED_TOOLS = {
    "latexmk": "--version",
    "pdflatex": "--version",
    "xelatex": "--version",
    "lualatex": "--version",
    "biber": "--version",
    "pygmentize": "-V",
}
REQUIRED_TOOLS_COMPRESS = {
    "gs": "--version",
}
REQUIRED_TOOLS_FORMAT = {
    "latexindent": "--version"
}
REQUIRED_TOOLS_SPELL = {
    "aspell": "--version"
}

MAX_WORKERS = os.cpu_count() or 1


@dataclass(order=True)
class BuildConfig:
    """Directory that contains the 'main.tex' file"""
    target_dir: Path
    """Optional: PDF engine (pdflatex, xetex)"""
    pdf_engine: Optional[str] = None
    """Optional: PDF compression quality (gs)"""
    pdf_compression_quality: Optional[str] = None
    """Optional: PDF output name"""
    pdf_output_name: Optional[str] = None
    """Optional: Labels"""
    labels: Optional[List[str]] = field(default_factory=list)


def run_command(cmd: List[str], cwd: Path = None, check: bool = True):
    cwd_str = f" in {cwd!r}" if cwd is not None else ''
    logger.debug(f"Running command: {(' '.join(cmd))!r}{cwd_str}")
    subprocess.run(cmd, cwd=cwd, check=check)

def check_dependencies(dependencies=None, optional_dependencies=None):
    if dependencies is None:
        dependencies = REQUIRED_TOOLS
    if optional_dependencies is None:
        optional_dependencies = REQUIRED_TOOLS_COMPRESS | REQUIRED_TOOLS_FORMAT | REQUIRED_TOOLS_SPELL
    missing = []
    for tool, tool_version_cmd in dependencies.items():
        if shutil.which(tool) is None:
            missing.append(tool)
        else:
            version_info = subprocess.run([tool, tool_version_cmd], capture_output=True, text=True)
            logger.debug(f"[dependency] {tool}: {version_info.stdout.strip()}")
    missing_optional = []
    for tool, tool_version_cmd in optional_dependencies.items():
        if shutil.which(tool) is None:
            missing_optional.append(tool)
        else:
            version_info = subprocess.run([tool, tool_version_cmd], capture_output=True, text=True)
            logger.debug(f"[dependency] {tool} (optional): {version_info.stdout.strip()}")
    if missing:
        logger.error(f"Missing required tools: {", ".join(missing)}")
        logger.warning("Please install them before running the build")
        sys.exit(1)
    logger.debug("All required dependencies found")
    if missing_optional:
        logger.warning(f"Missing optional tools: {", ".join(missing_optional)}")
        logger.warning("Install them to run all commands!")
    else:
        logger.debug("All optional dependencies found")

def find_targets() -> [BuildConfig]:
    targets: [BuildConfig] = []
    # Find all files starting with "config"
    logger.debug(f"Find targets...")
    for file_path in Path(".").glob("config*.py"):
        logger.debug(f"Found config: {file_path!r}")
        module_name = file_path.stem

        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Collect exported TARGETS values
        if hasattr(module, "TARGETS") and isinstance(module.TARGETS, list):
            targets.extend(module.TARGETS)
            logger.debug(f"Found targets: {module.TARGETS!r}")
    return targets


def clean_build():
    if DIST_DIR.exists():
        logger.info(f"Removing build directory {DIST_DIR}")
        shutil.rmtree(DIST_DIR)
    else:
        logger.info("No build directory to remove")


def run_latexmk(
    target_dir: Path,
    pdf_compression_quality: Optional[str]=None,
    pdf_output_name: Optional[str]=None,
    pdf_engine: Optional[str]=None,
    force=False,
    watch=False,
    watch_open=False,
    silent=False,
    verbose=False,
):
    output_dir = DIST_DIR / target_dir.name
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.debug(f"Building {target_dir.name!r} → {output_dir!r}")

    # Run latexmk from protocol folder
    try:
        run_command([
            "latexmk",
            *(["-verbose"] if verbose else []),                   # more detailed logs
            *(["-silent"] if silent else []),                     # hide detailed logs in terminal
            "-pdf",                                               # generate a pdf
            *(["-f", "-g"] if force else []),                     # force compilation
            *(["-pvc"] if watch else []),                         # continuous preview
            *([] if watch_open else ["-view=none"]),              # don't auto open pdf when doing continuous preview
            "-cd",                                                # change directory to the location of the .tex file before compiling
            f"-output-directory={output_dir}",                    # redirects all build artifacts to an out of source build directory
            *([f"-pdflatex={pdf_engine}"] if pdf_engine else []), # set LaTeX engine (pdflatex, xetex)
            "-shell-escape",                                      # escape code symbols that otherwise break LaTeX compiler
            f"-jobname={target_dir.name}",                        # output .pdf name
            "--file-line-error",                                  # show what file and what line actually threw an error
            "main.tex"
        ], cwd=target_dir)
    except subprocess.CalledProcessError:
        logger.error("LaTeX build failed!")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.error("LaTeX build was interupted!")
        sys.exit(1)

    pdf_file = output_dir / f"{target_dir.name}.pdf"

    pdf_file_base_name = pdf_output_name or target_dir.name
    pdf_file_dist = DIST_DIR / f"{pdf_file_base_name}.pdf"
    pdf_file_dist_uncompressed = DIST_DIR / f"{pdf_file_base_name}_uncompressed.pdf"

    if not pdf_file.exists():
        raise Exception("PDF not found, build failed")

    shutil.copy(pdf_file, pdf_file_dist)
    logger.info(f"Copied PDF to {pdf_file_dist!r}")

    if pdf_compression_quality is not None:
        shutil.move(pdf_file_dist, pdf_file_dist_uncompressed)
        logger.info(f"Moved that PDF to {pdf_file_dist_uncompressed!r}")
        run_ghostscript(pdf_file_dist_uncompressed, pdf_file_dist, quality=pdf_compression_quality)

        if os.path.getsize(pdf_file_dist_uncompressed) < os.path.getsize(pdf_file_dist):
            shutil.copy(pdf_file_dist_uncompressed, pdf_file_dist)
            logger.info(f"Copied uncompressed PDF to {pdf_file_dist!r} since its smaller")


def run_ghostscript(input_pdf_path: Path, output_pdf_path: Path, quality="printer"):
    if shutil.which("gs") is None:
        logger.warning("Did not find program to compress the PDF output")
        return None
    if not input_pdf_path.exists():
        raise FileNotFoundError(f"No PDF found to compress: {input_pdf_path!r}")
    try:
        run_command([
            "gs",
            "-sDEVICE=pdfwrite",                    # Generating a new PDF
            f"-dPDFSETTINGS=/{quality}",            # Preset for compression/quality
            #                                         - /screen:   lowest quality, smallest size
            #                                         - /ebook:    medium quality
            #                                         - /printer:  high quality
            #                                         - /prepress: very high quality (minimal compression)
            "-dNOPAUSE",                           # Prevents Ghostscript from waiting for user input between pages
            "-dQUIET",                             # Suppresses routine informational output (cleaner logs)
            "-dBATCH",                             # Ensures Ghostscript exits automatically after processing
            f"-sOutputFile={output_pdf_path}", # Output file path
            str(input_pdf_path),
        ])
        logger.info(f"Created compressed PDF: {output_pdf_path!r} (quality={quality!r})")
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Ghostscript compression failed") from e


def latexindent_tex_file(tex_file):
    run_command([
        "latexindent",
        "-w",
        "-s",
        "-l",
        str(tex_file)
    ], cwd=LATEX_INDENT_DIR)
    logger.info(f"Formatted {tex_file}")


def run_latexindent(target_dir: Optional[Path] = None):
    repo_root = ROOT_DIR
    exclude_dirs = [DIST_DIR.name]

    files = [
        tex_file for tex_file in (repo_root if target_dir is None else target_dir).rglob("*.tex")
        if not any(parent.name in exclude_dirs for parent in tex_file.parents)
    ]

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(latexindent_tex_file, files)

    # Cleanup ONCE (after all jobs)
    for tempRegex in ["*.bak*", "*indent.log"]:
        for bak_file in repo_root.rglob(tempRegex):
            bak_file.unlink()


def run_aspell(
    lang: str,
    extra_dicts: Optional[Iterable[str]] = None,
    tex_commands: Optional[Iterable[str]] = None,
    target_dir: Optional[Path] = None,
):
    cmd = ["aspell", f"--lang={lang}"]
    if extra_dicts is None:
        extra_dicts = ["en"]
    # aspell expects comma-separated list
    #cmd.append(f"--add-extra-dicts={",".join(extra_dicts)}")
    # append personal dictonary for the language
    lang_dir = LATEX_ASPELL_DIR / f"dict_{lang}"
    cmd.append(f"--personal={lang_dir}")
    cmd.append("--mode=tex")
    if tex_commands is None:
        tex_commands = [
            "addbibresource p",
            "alph p",
            "english p",
            "codefile opp",
            "color p",
            "csvautotabular pp",
            "definecolor ppp",
            "GenericError pp",
            "gls p",
            "IfFileExists p",
            "inputminted opp",
            "mintinline pp",
            "newacronym p p P",
            "newcommand pp",
            "requirecommand p",
            "textcolor pP",
            "texttt p",
            "todo p",
            "sisetup p",
        ]
    # aspell expects comma-separated list
    cmd.extend([f"--add-tex-command={tex_command}" for tex_command in tex_commands])

    repo_root = ROOT_DIR
    exclude_dirs = [DIST_DIR.name]
    for tex_file in (repo_root if target_dir is None else target_dir).rglob("*.tex"):
        if any(parent.name in exclude_dirs for parent in tex_file.parents):
            continue
        run_command([*cmd, "check", str(tex_file)])
        # clean up any remaining .bak files
        for tempRegex in ["*.bak*"]:
            for bak_file in tex_file.parent.rglob(tempRegex):
                bak_file.unlink()


def main():
    parser = argparse.ArgumentParser(description="LaTeX build system")
    parser.add_argument('-v', '--verbose', action='store_true', help="Show more logs")
    parser.add_argument(
        "--log-file",
        type=str,
        default=None,
        help="create log file"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.0.8"
    )

    # subparser
    subparsers = parser.add_subparsers(dest="command")

    # shared arguments
    target_options = argparse.ArgumentParser(add_help=False)
    target_options.add_argument("target_label", nargs="?", help="choose a specific target via the directory path or by using a label (using the colon prefix e.g. ':LABEL')")

    target_options_engine = argparse.ArgumentParser(add_help=False)
    target_options_engine.add_argument("-e", "--engine", nargs="?", help="pdf engine (xetex, pdflatex)", default=False)

    # info
    info_parser = subparsers.add_parser("info")
    info_parser.add_argument("--targets", action="store_true", help="show targets (default: %(default)s)", default=True)

    # build
    build_parser = subparsers.add_parser("build", parents=[target_options, target_options_engine])
    build_parser.add_argument("-f", "--force", action="store_true", help="force build", default=False)
    build_parser.add_argument("-w", "--watch", action="store_true", help="continuous build", default=False)
    build_parser.add_argument("-wo", "--watch-open", action="store_true", help="continuous build and open PDF", default=False)
    build_parser.add_argument("-s", "--silent", action="store_true", help="hide all logs in terminal", default=False)

    # clean
    subparsers.add_parser("clean")

    # format
    subparsers.add_parser("format", parents=[target_options])

    # spell
    spell_parser = subparsers.add_parser("spell", parents=[target_options])
    spell_parser.add_argument("--lang", nargs="?", help="use a specific language dictionary (default: %(default)s)", default="en")

    # ---------------------------------------------------------------

    # parse arguments
    args = parser.parse_args()

    # add console logger
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    console.setFormatter(logger_format)
    logger.addHandler(console)

    # add file logger if specified (always debug level)
    if args.log_file:
        file_handler = logging.FileHandler(args.log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logger_format)
        logger.addHandler(file_handler)

    # parser arguments check
    logger.debug(args)

    # general dependency check
    check_dependencies()

    targets = find_targets()
    selected_targets: Optional[List[BuildConfig]] = None
    if hasattr(args, "target_label") and args.target_label:
        if args.target_label.startswith(":"):
            label = args.target_label[1:]
            selected_targets = [tar for tar in targets if label in tar.labels]
            if len(selected_targets) == 0:
                logger.error(f"Unable to find any target using the label {label!r}!")
                sys.exit(1)
        else:
            try:
                selected_targets = [next(tar for tar in targets if tar.target_dir.name == args.target_label)]
            except StopIteration:
                logger.error(f"Unable to find target {args.target_label!r}!")
                sys.exit(1)
        logger.debug(f"Selected targets: {selected_targets}")

    if args.command == "info":
        if args.targets:
            print('Targets:')
            for target in targets:
                print(f"- {target.target_dir.name} {target.labels}: {target}")
    elif args.command == "clean":
        clean_build()
    elif args.command == "format":
        if selected_targets is not None:
            for selected_target in selected_targets:
                run_latexindent(target_dir=selected_target.target_dir)
        else:
            run_latexindent()
    elif args.command == "spell":
        if selected_targets is not None:
            for selected_target in selected_targets:
                run_aspell(args.lang, target_dir=selected_target.target_dir)
                run_latexindent(target_dir=selected_target.target_dir)
        else:
            run_aspell(args.lang)
    elif args.command == "build":
        build_targets = targets if selected_targets is None else selected_targets

        # exit for incompatible options
        if len(build_targets) > 1 and (args.watch or args.watch_open):
            logger.error(f"Watching changes is not supported for multiple targets! ({len(build_targets)})")
            sys.exit(1)

        def build_target(target):
            run_latexmk(
                target.target_dir,
                pdf_engine=target.pdf_engine or args.engine,
                pdf_compression_quality=target.pdf_compression_quality,
                pdf_output_name=target.pdf_output_name,
                force=args.force,
                watch=args.watch or args.watch_open,
                watch_open=args.watch_open,
                silent=args.silent,
                verbose=args.verbose,
            )

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for f in as_completed([
                executor.submit(build_target, t)
                for t in build_targets
            ]):
                f.result()

    elif args.command is None:

        def build_target(target):
            run_latexmk(
                target.target_dir,
                pdf_engine=target.pdf_engine,
                pdf_compression_quality=target.pdf_compression_quality,
                pdf_output_name=target.pdf_output_name,
                verbose=args.verbose,
            )

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            for f in as_completed([
                executor.submit(build_target, t)
                for t in targets
            ]):
                f.result()

    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.error("LaTeX build was interupted!")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error")
        sys.exit(1)
