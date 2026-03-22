# LaTeX templates (modern)

## Build `.pdf`

Running the following commands will create a `.pdf`/`_compressed.pdf` in `build` for all targets listed in `config.py`.

**Linux:**

```sh
./build.py
# a specific target
./build.py protocol_00_example
```

Requires:

- Build script: `python3`
- LaTeX compiler and packages: `latexmk`, `texlive-full` (on arch: `texlive`, `texlive-langgerman`, `texlive-langenglish`)
- Citations: `biber`
- Code Syntax Highlighting: `pygmentize` (on arch: `python-pygments`, on debian: `pip install Pygments`)

> Format: `perl-file-homedir`, `perl-yaml-tiny`

**Windows:**

```sh
python build.py
# a specific target
python build.py protocol_00_example
```
