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

<details>
<summary>Linux requirements:</summary>

- LaTeX compiler and packages: `latexmk`, `texlive-full` (on arch: `texlive`, `texlive-langgerman`, `texlive-langenglish`)
- Citations: `biber`
- Python: `python` (on arch: `python`, on debian: `python3`)
- Code Syntax Highlighting: `pygmentize` (on arch: `python-pygments`, on debian: `pip install Pygments`)

> Format: `perl-file-homedir`, `perl-yaml-tiny`
</details>

<details>
<summary>Windows requirements:</summary>

- Python: `winget install Python3`/`winget install Python.Python.3.14`)

  ```sh
  python --version
  ```

  ```
  Python 3.14.5
  ```


  - Code Syntax Highlighting: `python -m pip install Pygments`
    ```sh 
    pygmentize -V
    ```

    ```
    Pygments version 2.20.0, (c) 2006-present by Georg Brandl, Matthäus Chajdas and contributors.
    ```

- LaTeX: `winget install MiKTeX.MiKTeX` & `winget install StrawberryPerl.StrawberryPerl`

  ```sh
  latexmk --version
  ```

  ```
  Initial Win CP for (console input, console output, system): (CP437, CP65001, CP1252)
  I changed them all to CP1252
  Latexmk, John Collins, 9 March 2026. Version 4.88
  Reverting Windows console CPs to (in,out) = (437,65001)
  latexmk: major issue: So far, you have not checked for MiKTeX updates.
  ```

  ```sh
  biber --version
  ```

  ```
  biber version: 2.21
  biber: major issue: So far, you have not checked for MiKTeX updates.
  ```

  ```sh
  perl --version
  ```

  ```
  This is perl 5, version 42, subversion 2 (v5.42.2) built for MSWin32-x64-multi-thread
  
  Copyright 1987-2026, Larry Wall
  
  Perl may be copied only under the terms of either the Artistic License or the
  GNU General Public License, which may be found in the Perl 5 source kit.
  
  Complete documentation for Perl, including FAQ lists, should be found on
  this system using "man perl" or "perldoc perl".  If you have access to the
  Internet, point your browser at https://www.perl.org/, the Perl Home Page.
  ```

  ```sh
  pdflatex --version
  ```

  ```
  MiKTeX-pdfTeX 4.23 (MiKTeX 25.12)
  © 1982 D. E. Knuth, © 1996-2025 Hàn Thế Thành
  TeX is a trademark of the American Mathematical Society.
  using bzip2 version 1.0.8, 13-Jul-2019
  compiled with curl version 8.4.0; using libcurl/8.4.0 Schannel
  compiled with expat version 2.5; using expat_2.5.0
  compiled with jpeg version 9.5
  compiled with liblzma version 50040002; using 50040002
  compiled with libpng version 1.6.44; using 1.6.44
  compiled with libressl version LibreSSL 3.8.1; using LibreSSL 3.8.1
  compiled with MiKTeX Application Framework version 4.8; using 4.8
  compiled with MiKTeX Core version 4.24; using 4.24
  compiled with MiKTeX Archive Extractor version 4.1; using 4.1
  compiled with MiKTeX Package Manager version 4.10; using 4.10
  compiled with uriparser version 0.9.7
  compiled with xpdf version 4.04
  compiled with zlib version 1.2.13; using 1.2.13
  pdflatex: major issue: So far, you have not checked for MiKTeX updates.
  ```

  > 1. On the first run of e.g. `latexmk --version` a window will pop up and ask for confirmation.
  >    By disabling *Always show dialog* this will automatically install packages in the future.
  > 2. Before doing anything MiKTeX needs to be updated/initialized
  >
  >    1. Start *MiKTeX Console*
  >    2. Click *Check for updates* on the *Welcome* page
  >    3. When its done it will have a link to an *Updates page* right below the button, click it
  >    4. Click *Update now* on the *Updates* page
  >    5. Close the window when prompted (after all updates are done)
  > 3. Enable to install missing packages on the fly
  >    1. Start *MiKTeX Console*
  >    2. Go to the *Settings* page
  >    3. Check under *Package installation* the option *Always* to install missing packages automatically
  > 4. If encountering missing packages here are some packages that can be manually installed to fix these issues (under *MiKTeX Console* and the *Packages* page):
  >    1. `File 'punec.def' not found`: `hyperref`

- [Optional] gs: https://github.com/qpdf/qpdf/releases/tag/latest, download *Ghostscript AGPL Release*  (*Ghostscript $VERSION for Windows (64 bit)*) and run installer

  ```sh
  gs --version
  ```

  ```
  10.07.1
  ```

  > Since it gets installed under the name `gswin64c` go to the install directory `C:\Program Files\gs\gs$VERSION\bin` and copy this file and name it `gs`

- [Optional] qpdf: https://github.com/qpdf/qpdf/releases/tag/latest, download and run installer `Qpdf-$VERSION-msvc64.exe`

  ```sh
  qpdf --version
  ```

  ```
  qpdf version 12.3.2
  Run qpdf --copyright to see copyright and license information.
  ```
</details>
