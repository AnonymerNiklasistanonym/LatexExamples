#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

ROOT_DIR = Path(__file__).parent
PROTOCOL_DIR_PREFIX = "protocol_"

GROUP_NAME = "3"
PROTOCOL_NAMES = {
    '00': 'example',
}

@dataclass(order=True)
class BuildConfig:
    """Directory that contains the 'main.tex' file"""
    target_dir: Path
    """Optional: PDF compression quality (gs)"""
    pdf_compression_quality: Optional[str] = None
    """Optional: PDF output name"""
    pdf_output_name: Optional[str] = None


def get_protocol_output_name(protocol_dir: Path) -> Optional[str]:
    """
    [Versuch]-gr[Gruppen Nr]
    Bsp: Protokollanalyse-gr3.pdf
    """
    protocol_number = protocol_dir.name.removeprefix(PROTOCOL_DIR_PREFIX)
    if protocol_number not in PROTOCOL_NAMES:
        return None
    return f"{PROTOCOL_NAMES[protocol_number]}-gr{GROUP_NAME}"


def discover_targets(root: Path) -> List[BuildConfig]:
    return sorted(
        (
            BuildConfig(p, pdf_compression_quality="prepress", pdf_output_name=get_protocol_output_name(p))
            for p in root.iterdir()
            if p.is_dir() and p.name.startswith(PROTOCOL_DIR_PREFIX)
        ),
        key=lambda x: x.target_dir.name
    )

CUSTOM_TARGETS = [
    discover_targets(ROOT_DIR),
    BuildConfig(ROOT_DIR / "example_protocol_single", pdf_compression_quality="prepress", pdf_output_name="protocol_your_name")
]
