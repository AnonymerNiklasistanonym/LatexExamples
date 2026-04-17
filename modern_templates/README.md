# LaTeX templates (modern)

## Build `.pdf`

Running the following commands will create `.pdf`/`_compressed.pdf` files in `build` for all or specific targets listed in `config.py`.

**Linux:**

```sh
./latex.py
# or a specific target
./latex.py build protocol
# automatically build latest version after file changes
./latex.py build --watch protocol
./latex.py build --watch-open protocol
```

Requires:

- Build script: `python3`
- LaTeX compiler and packages: `latexmk`, `texlive-full` (on arch: `texlive`, `texlive-langgerman`, `texlive-langenglish`)
- Citations: `biber`
- Code Syntax Highlighting: `pygmentize` (on arch: `python-pygments`, on debian: `pip install Pygments`)

> Format: `perl-file-homedir`, `perl-yaml-tiny`

**Windows:**

```sh
python latex.py
# or a specific target
python latex.py build protocol
# automatically build latest version after file changes
python latex.py build --watch protocol
python latex.py build --watch-open protocol
```

## Spellcheck

```sh
# Get source code
git clone https://github.com/ggml-org/llama.cpp.git
```

```sh
# Update source code and build
cd llama.cpp
git pull
cmake -B build -DCMAKE_BUILD_TYPE=Release -DLLAMA_CURL=ON -DLLAMA_BUILD_TESTS=OFF && cmake --build build -j
```

```sh
# Start llama.cpp web server
cd llama.cpp
./build/bin/llama-server -hf unsloth/gemma-4-E4B-it-GGUF:UD-Q4_K_XL --port 3000 --host 0.0.0.0
```

```sh
# Start spellchecking by doing web requests to that web server (logfile and target are optional)
uv run ./latex/proofreader/llamacpp_proofreader.py --logfile out.log protocol_01
```
