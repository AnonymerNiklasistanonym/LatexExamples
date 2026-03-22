#!/usr/bin/env python3
from pathlib import Path

ROOT_DIR = Path(__file__).parent

# Example for directories with a main.tex that are manually added

PAPER_DIR = ROOT_DIR / "paper"
LERNTAGEBUCH_DIR = ROOT_DIR / "lerntagebuch"

TARGET_DIRS = [PAPER_DIR, LERNTAGEBUCH_DIR]

# Example for directories with a main.tex that are automatically discovered

PROTOCOL_DIR_PREFIX = "protocol_"

PROTOCOL_DIRS = sorted([p for p in ROOT_DIR.iterdir() if p.is_dir() and p.name.startswith(PROTOCOL_DIR_PREFIX)])

TARGET_DIRS = PROTOCOL_DIRS

# Combine them all:

TARGET_DIRS = [PAPER_DIR, LERNTAGEBUCH_DIR, *PROTOCOL_DIRS]
