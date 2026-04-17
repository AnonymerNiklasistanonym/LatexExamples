#!/usr/bin/env pwsh

latexmk -pdf -outdir=build -shell-escape main.tex
latexmk -pdf -outdir=build -shell-escape -jobname=main-handout -pdflatex="pdflatex %O `"`\def\HANDOUTMODE{}`\input{%S}`"" main.tex
