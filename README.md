# LaTeXExamples

This repository contains Latex example scripts and a tutorial of how to compile and edit them.

## Setup on Windows

To compile and edit them without too much pain you need to install the folowing two programs:

- [TeXstudio](https://www.texstudio.org/)
- [MiKTeX](https://miktex.org/download) (while the installation set `always`for the option to *install packages on the fly*)

Then you can for once compile any LaTeX file via command line:

```bash
miktex-pdflatex latexFile.tex
```

Or open TeXstudio and press F5 after creating a new file to directly compile and view it.

## Compile the TeX file in TeXstudio

Open a file or create one and then press the green `Build and view` button in the menu bar or simply press `F5` to directly view the compiled PDF document.

With one additional click you can even open it instantly with an external PDF viewer. And if you only want to compile it just press `F6` instead of `F5`.

## Configure TeXstudio

### Change the language

To change the language of the editor (for example you want to edit a german instead of an english one).

You just click in the menu bar `Options`, then `Configure TeXstudio` and then select `Language Checking`. There you can change in the section `Default Language` the language to your desired language.
