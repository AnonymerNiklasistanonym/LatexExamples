#!/usr/bin/env python3

# /// script
# dependencies = [
#   "transformers",
#   "torch",
# ]
# ///

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "oliverguhr/spelling-correction-german-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def spell_check(text: str):
    inputs = tokenizer(f"correct spelling: {text}", return_tensors="pt")

    outputs = model.generate(**inputs)
    corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if corrected_text.startswith("Spelling "):
        corrected_text = corrected_text[len("Spelling "):]
    return corrected_text


if __name__ == "__main__":
    example = "Das ist ein Beispeil mit Fehlern."
    print(f"spell check {example=} ({len(example)=})")
    correct = spell_check(example)
    print(f"spell check result: {correct=}")
