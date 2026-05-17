#!/usr/bin/env python3

from pathlib import Path

# Local application/library
from latex import BuildConfig

ROOT_DIR = Path(__file__).parent

TARGETS = [
    BuildConfig(ROOT_DIR / "motivationsschreiben_v1", pdf_output_name="motivationsschreiben_v1", pdf_compression_quality="prepress", labels="motivationsschreiben")
]
