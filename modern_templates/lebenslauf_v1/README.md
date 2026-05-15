# Lebenslauf (v1)

[Example](./example.pdf)

## Build

The following command creates a `build/lebenslauf.pdf` file:

```sh
latexmk -pdf -cd -output-directory=build -jobname="lebenslauf" --file-line-error main.tex
```

**Compress:**

```sh
gs -o lebenslauf.pdf -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress -dNOPAUSE -dBATCH -dQUIET build/lebenslauf.pdf
```

## Clean

```sh
rm -rf build
```

## Custom Data

1. Copy `template` directory and name it `data`
2. Edit the files inside `data` with your private personal data (the directory is *gitignored* by default!)
