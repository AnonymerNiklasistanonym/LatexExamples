#!/usr/bin/env python3

# /// script
# dependencies = [
#   "openai",
# ]
# ///

# uv run spellcheck_llamacpp.py

from openai import OpenAI

# Port on which llama.cpp was started
PORT = 3000

# Model with which llama.cpp was started
MODEL = "unsloth/gemma-4-E4B-it-GGUF:UD-Q4_K_XL"

# Tell the OpenAI client to look at the local server (no API key required) instead of openai.com
client = OpenAI(base_url=f"http://localhost:{PORT}/v1", api_key='ignored-by-local-server')


def get_llm_response(prompt: str):
    try:
        # The client methods match the standard OpenAI library calls
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        # Extract the content from the structured response
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error interacting with the server: {e}")
        return None


# --- Execution ---
user_prompt = "Write a short, motivational haiku about programming."
response = get_llm_response(user_prompt)
print(response)
