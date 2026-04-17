#!/usr/bin/env python3

# /// script
# dependencies = [
#   "ollama",
# ]
# ///

from ollama import chat
from typing import Optional

MODEL="gemma3:4b"

def spell_check(text: str, acronyms: Optional[str] = None):
    prompt = f"""
    Act as a professional editor for LaTeX documents.
    Please proofread the following text in LaTeX format for spelling, grammar, and punctuation mistakes.
    Keep all LaTeX commands, newlines, spaces that are not text related intact.
    {f"Use the following LaTeX glossary acronyms correctly: {acronyms}" if acronyms else ''}
    Return the corrected text.

    LaTeX document part:
    {text}
    """

    response = chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.message.content


if __name__ == "__main__":
    example = "Das ist ein Beispeil mit Fehlern."
    print(f"spell check {example=} ({len(example)=})")
    correct = spell_check(example)
    print(f"spell check result: {correct=}")
