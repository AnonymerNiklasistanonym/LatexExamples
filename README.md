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

## Links

- (introduction) [LaTeX introduction by sharelatex](https://www.sharelatex.com/learn/Main_Page)
- (other templates) [Some real math formulas by MartinThoma](https://github.com/MartinThoma/LaTeX-examples/blob/master/cheat-sheets/analysis/Analysis_Wichtige_Formeln.tex) and more in the [Repository](https://github.com/MartinThoma/LaTeX-examples)
- (presentation templates) [Presentation templates by overleaf with previews in the browser](https://www.overleaf.com/gallery/tagged/presentation)
- (other templates) [Other templates by overleaf with previews in the browser](https://www.overleaf.com/gallery)
- (other templates) [Other templates with previews in the glossar by mhyee](https://github.com/mhyee/latex-examples)
- (advanced) [TikZ package introduction by sharelatex](https://www.sharelatex.com/learn/TikZ_package)
- (advanced) [TikZ preview website](http://www.tlhiv.org/ltxpreview/)

## How to create simple automatas

### 1. Step - Create one

Create with this website simple and fast your automata: http://madebyevan.com/fsm/ (it's even [here on GitHub](https://github.com/evanw/fsm)).

Then download the automatically created LaTeX code of this automata.

### 2. Step - Export/Edit or optimize

On this website you can now edit special characters or more (you can also do this in TeXstudio, but I prefer it this way: http://www.tlhiv.org/ltxpreview/.

*(don't forget to add the needed packages!)*

Now you can copy the code and import it directly into your LaTeX document - or you can download it as a vector graphic if you want.

### Error handling:

If the website ever would not work any more or you want to do it offline you can use the backup in the directory [`automatas`](automatas).

## Presentation templates

- Classic simple design: https://www.overleaf.com/latex/templates/beamer-presentation/zxrfltwmbcrt
- Modern design: https://www.overleaf.com/latex/templates/metropolis-beamer-theme/qzyvdhrntfmr
