# example-presentation-raii

## Build

```sh
mkdir -p build
latexmk -pdf -outdir=build gotham-example169transp.tex
```

```sh
# clean build files
latexmk -C -outdir=build
rm -rf build
```

### Windows

```sh
# minted
python -m venv venv_minted
.\venv_minted\Scripts\Activate.ps1
pip install Pygments
# perl
winget install StrawberryPerl.StrawberryPerl
# latexmk
winget install MiKTeX.MiKTeX
# alt
set TEXMF_OUTPUT_DIRECTORY=build
latexmk -pdf -shell-escape -outdir=build main.tex
```
