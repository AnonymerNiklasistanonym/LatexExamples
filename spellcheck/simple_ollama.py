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
    Correct German spelling in this LaTeX document.
    Keep all LaTeX commands intact.
    Don't use any formatting in the output so it can be used to replace the original document in git.
    {f"Use the following acronyms correctly: {acronyms}" if acronyms else ''}

    Document:
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
