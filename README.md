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

## Configure TeXstudio

### Change the language

To change the language of the editor (for example you want to edit a german instead of an english one).

You just click in the menu bar `Options`, then `Configure TeXstudio` and then select `Language Checking`. There you can change in the section `Default Language` the language to your desired language.