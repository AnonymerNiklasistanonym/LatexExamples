#!/usr/bin/env python3

# /// script
# dependencies = [
#   "openai",
# ]
# ///

# uv run spellcheck_llamacpp.py

# Necessary standard library imports
import argparse
import os
from pathlib import Path
import logging

# External dependency for the API client
from openai import OpenAI

# --- Configuration ---
PORT = 3000
MODEL = "unsloth/gemma-4-E4B-it-GGUF:UD-Q4_K_XL"

ROOT_DIR = Path(__file__).parent.parent.parent
EXCLUDE_DIRS = ["latex", "build", ".git"]

logger = logging.getLogger("latex_proofreader")
logger.setLevel(logging.DEBUG)

# Tell the OpenAI client to look at the local server (no API key required)
# The base_url must point to the server's endpoint (/v1)
try:
    client = OpenAI(base_url=f"http://localhost:{PORT}/v1", api_key='ignored-by-local-server')
except Exception as e:
    logger.error(f"FATAL ERROR: Could not initialize OpenAI client. Is llama-server running on port {PORT}? Error: {e}")
    exit(1)


def spell_check(text: str, acronyms: str = None) -> str:
    """
    Uses the local llama-server API to proofread and correct LaTeX documents.
    """
    # 1. Construct the detailed prompt (System instruction + User input)
    system_prompt = (
        "Act as a professional editor/proof reader for scientific LaTeX documents. "
        "Please proofread the following text in LaTeX format for spelling, grammar, and punctuation mistakes. "
        "Keep all LaTeX commands, newlines, and spaces intact (keep in mind that there are verbatim environments like codeblock, minted, mintinline, ... that do not need spellchecking). "
        "Do not translate comments that won't be rendered (like '\\todo{...}' or '% ...'). "
        "If you do big changes add a \\todo{Previously: $PreviousContent - $Reason} + [NEWLINE] in front of the corrected and replaced sentence instead of the previous one so it can be easily manually audited. "
        "If you find any quotes like \"word\" or 'word' replace them with \\enquote{word} (if again not part of e.g. an verbatim environment like codeblock, minted, mintinline, ...) as well as any _ and replace them with \\_ (if it was part of the text and not a command or \\input) since LaTeX has problems with that. "
        "Replace any acronyms that do not use \\gls{acronym} if you find any corresponding existing acronym definitions (like \\newacronym{tcp}{TCP}{Transport Layer Protocol} means replace TCP with \\gls{tcp} if its not part of a section or listing/figure/table). "
        "If you notice any incorrect facts add a \\todo{Incorrect: $Reason} in front of the factually incorrect sentence."
    )

    # Add acronym glossary if provided
    acronyms_glossary = ""
    if acronyms:
        acronyms_glossary = f"Use the following LaTeX glossary acronyms correctly:\n{acronyms}\n"

    # Combine everything into the final user input
    prompt_content = f"{acronyms_glossary}\nLaTeX document snippet:\n{text}"

    # 2. Call the local LLM API
    try:
        messages = [
            # Use the system role for instructions
            {"role": "system", "content": system_prompt},
            # Use the user role for the document content
            {"role": "user", "content": prompt_content}
        ]
        logger.debug(messages)

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.1,  # Use a lower temperature for deterministic editing tasks
            max_tokens=4096  # Increase max_tokens to ensure full document correction
        )

        # 3. Extract the corrected text
        logger.debug(response)
        return response.choices[0].message.content

    except Exception as e:
        logger.error("\n" + "=" * 50)
        logger.error(f"API CALL FAILED. Check if llama-server is running and accessible.")
        logger.error(f"Error: {e}")
        logger.error("=" * 50 + "\n")
        return text  # Return original text if the API fails


if __name__ == "__main__":
    repo_root = ROOT_DIR
    exclude_dirs = EXCLUDE_DIRS

    parser = argparse.ArgumentParser(description='LaTeX proofreader')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show more logs')
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.0.1"
    )
    parser.add_argument('--logfile', type=str, help='enable logging to a file')
    parser.add_argument('target_dir', nargs="?", help='proofread only a specific target directory')

    # parse arguments
    args = parser.parse_args()

    # update log level depending on arguments
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO if not args.verbose else logging.DEBUG)
    console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M'))
    logger.addHandler(console_handler)

    # create logfile if requested
    if args.logfile:
        file_handler = logging.FileHandler(args.logfile)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M'))
        logger.addHandler(file_handler)

    # parser arguments check
    logger.debug(args)

    target = ROOT_DIR
    if hasattr(args, "target_dir") and args.target_dir:
        target = ROOT_DIR / args.target_dir
        if not target.exists:
            logger.error(f"Target directory does not exist {args.target!r}!")
            sys.exit(1)

    # 1. Read acronyms glossary
    acronym_path = repo_root / "latex" / "acronyms.tex"
    if acronym_path.exists():
        with open(acronym_path, "r", encoding="utf-8") as f:
            acronyms = f.read()
    else:
        acronyms = None
        logger.warn(f"Acronyms file not found at {acronym_path}. Proceeding without glossary.")

    # 2. Iterate through all .tex files
    tex_files_updated = 0
    for tex_file in target.rglob("*.tex"):
        # Skip files in excluded directories
        if any(parent.name in exclude_dirs for parent in tex_file.parents):
            continue

        logger.info(f"Processing: {tex_file}")

        # Read content
        try:
            with open(tex_file, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            logger.error(f"Could not read file {tex_file}: {e}")
            continue

        # Run the spell check using the LLM API
        text_corrected = spell_check(text, acronyms)

        # Write back the corrected content
        try:
            with open(tex_file, "w", encoding="utf-8") as f:
                f.write(text_corrected)
                # Ensure the file ends with a newline character
                if not text_corrected.endswith(os.linesep):
                    f.write(os.linesep)

            logger.info(f"Successfully updated {tex_file}")
            tex_files_updated += 1
        except Exception as e:
            logger.error(f"Could not write to file {tex_file}: {e}")

    logger.info(f"\n--- Process Complete. Total files updated: {tex_files_updated} ---")
