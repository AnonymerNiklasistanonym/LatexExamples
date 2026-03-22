#!/usr/bin/env python3
from config import TARGET_DIRS
from pathlib import Path
import shutil
import subprocess
import sys

ROOT_DIR = Path(__file__).parent
DIST_DIR = ROOT_DIR / "build"

REQUIRED_TOOLS = ["latexmk", "pdflatex", "biber", "pygmentize"]
REQUIRED_TOOLS_COMPRESS = ["gs"]
REQUIRED_TOOLS_FORMAT = ["latexindent"]


def check_dependencies(dependencies=REQUIRED_TOOLS, optional_dependencies=[*REQUIRED_TOOLS_COMPRESS, *REQUIRED_TOOLS_FORMAT]):
    missing = []
    for tool in dependencies:
        if shutil.which(tool) is None:
            missing.append(tool)
    missing_optional = []
    for tool in optional_dependencies:
        if shutil.which(tool) is None:
            missing_optional.append(tool)
    if missing:
        print("[ERROR] Missing required tools:", ", ".join(missing))
        print("Please install them before running the build")
        sys.exit(1)
    print("[INFO] All required dependencies found")
    if missing_optional:
        print("[WARN] Missing optional tools:", ", ".join(missing_optional))
        print("Install them to run all commands")
    else:
        print("[INFO] All optional dependencies found")

def run_latexmk(dir: Path):
    OUTPUT_DIR = DIST_DIR / dir.name
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Building {dir.name} → {OUTPUT_DIR}")

    # Run latexmk from protocol folder
    try:
        subprocess.run([
            "latexmk",
            "-pdf",                              # generate a pdf
            "-cd",                               # change directory to the location of the .tex file before compiling
            f"-output-directory={OUTPUT_DIR}",   # redirects all build artifacts to an out of source build directory
            "-pdflatex=pdflatex",                # set LaTeX engine
            "-shell-escape",                     # escape code symbols that otherwise break LaTeX compiler
            f"-jobname={dir.name}",              # output .pdf name
            "main.tex"
        ], cwd=dir, check=True)
    except subprocess.CalledProcessError:
        print("[ERROR] LaTeX build failed!")
        sys.exit(1)
    except KeyboardInterrupt:
        print("[ERROR] LaTeX build was interupted!")
        sys.exit(1)

    PDF_FILE = OUTPUT_DIR / f"{dir.name}.pdf"
    PDF_FILE_DIST = DIST_DIR / f"{dir.name}.pdf"

    if PDF_FILE.exists():
        shutil.copy(PDF_FILE, PDF_FILE_DIST)
        print(f"[INFO] Copied PDF to {PDF_FILE_DIST}")
        compress_pdf(PDF_FILE_DIST)
    else:
        raise Exception("PDF not found, build failed")


def compress_pdf(input_pdf_path: Path):
    if shutil.which("gs") is None:
        print("[WARN] Did not find program to compress the PDF output")
        return
    if not input_pdf_path.exists():
        raise FileNotFoundError(f"[ERROR] No PDF found to compress: {input_path}")

    PDF_COMPRESSED_FILE = input_pdf_path.with_name(input_pdf_path.stem + "_compressed.pdf")

    try:
        subprocess.run([
            "gs",
            "-sDEVICE=pdfwrite",                    # Generating a new PDF
            "-dPDFSETTINGS=/printer",               # Preset for compression/quality
            #                                         - /screen:   lowest quality, smallest size
            #                                         - /ebook:    medium quality
            #                                         - /printer:  high quality
            #                                         - /prepress: very high quality (minimal compression)
            "-dNOPAUSE",                           # Prevents Ghostscript from waiting for user input between pages
            "-dQUIET",                             # Suppresses routine informational output (cleaner logs)
            "-dBATCH",                             # Ensures Ghostscript exits automatically after processing
            f"-sOutputFile={PDF_COMPRESSED_FILE}", # Output file path
            str(input_pdf_path),
        ], check=True)
        print(f"[INFO] Created compressed PDF to {PDF_COMPRESSED_FILE}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Ghostscript compression failed") from e

    return PDF_COMPRESSED_FILE


def clean_build():
    if DIST_DIR.exists():
        print(f"[INFO] Removing build directory {DIST_DIR}")
        shutil.rmtree(DIST_DIR)
    else:
        print("[INFO] No build directory to remove")


def format():
    repo_root = ROOT_DIR
    exclude_dirs = {"build", ".git"}
    for tex_file in repo_root.rglob("*.tex"):
        if any(parent.name in exclude_dirs for parent in tex_file.parents):
            continue
        subprocess.run([
            "latexindent",
            "-w",  # overwrite
            "-s",  # silent
            "-l",  # suppress log
            str(tex_file)
        ])
        # Clean up any remaining .bak and indent.log files
        for tempRegex in ["*.bak*", "*indent.log"]:
            for bak_file in repo_root.rglob(tempRegex):
                bak_file.unlink()
        print(f"[INFO] Formatted {tex_file}")


def main():
    check_dependencies()

    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "clean":
            clean_build()
        elif sys.argv[1].lower() == "format":
            format()
        else:
            for target in TARGET_DIRS:
                if sys.argv[1].lower() == target.name.lower():
                    run_latexmk(target)
    else:
        for target in TARGET_DIRS:
            run_latexmk(target)


if __name__ == "__main__":
    main()
