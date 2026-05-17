# LaTeX templates (modern)

## Build `.pdf`

Running the following commands will create `.pdf`/`_compressed.pdf` files in `build` for all or specific targets listed in `config*.py` files.

```sh
# assumes this is python3.11 or higher
python latex.py
# get list of all targets
python latex.py info
# build a specific target ('./protocol/main.tex') given its directory name
python latex.py build protocol
# automatically build latest version after file changes
python latex.py build --watch protocol
python latex.py build --watch-open protocol
# if the target has a label in the config this can also be used
# (all targets with this label 'protocol' will be built)
python latex.py build :protocol
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
