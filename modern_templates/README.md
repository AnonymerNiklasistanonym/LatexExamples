# LaTeX templates (modern)

## Build `.pdf`

Running the following commands will create `.pdf`/`_compressed.pdf` files in `build` for all or specific targets listed in `config.py`.

```sh
# assumes this is python3.11 or higher
python latex.py
# or a specific target
python latex.py build protocol
# automatically build latest version after file changes
python latex.py build --watch protocol
python latex.py build --watch-open protocol
```

> To customize the `.pdf` viewer for watch-open:
>
> 1. Create a home directory file: `$HOME/.latexmkrc`
>
> 2. Set your custom `.pdf` viewer program inside:
>
>    ```sh
>    $pdf_previewer = 'start okular';
>    ```

**Linux requirements:**

- LaTeX compiler and packages: `latexmk`, `texlive-full` (on arch: `texlive`, `texlive-langgerman`, `texlive-langenglish`)
- Citations: `biber`
- Code Syntax Highlighting: `pygmentize` (on arch: `python-pygments`, on debian: `pip install Pygments`)

> Format: `perl-file-homedir`, `perl-yaml-tiny`

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
