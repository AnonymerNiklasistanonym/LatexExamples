# -------------------------------
# Configuration
# -------------------------------
MAIN      := main
BUILDDIR  := build
RESDIR    := res
CONTENTDIR:= section
LATEXMK   := latexmk
INKSCAPE  := inkscape

SPELLCHECK = aspell
SPELLCHECK_LANG = en_US
SPELLCHECK_CUSTOM_DICT = custom_dict.txt

SVG_FILES := $(wildcard $(RESDIR)/*.svg)
TEX_FILES = $(MAIN).tex $(wildcard $(CONTENTDIR)/*.tex)
PDF_SVGS  := $(SVG_FILES:.svg=.pdf)

# -------------------------------
# Default target
# -------------------------------
.PHONY: all $(BUILDDIR)/$(MAIN).pdf $(BUILDDIR)/$(MAIN)-handout.pdf
all: $(BUILDDIR)/$(MAIN).pdf $(BUILDDIR)/$(MAIN)-handout.pdf

# -------------------------------
# Directories
# -------------------------------
$(BUILDDIR):
	mkdir -p $(BUILDDIR)

# -------------------------------
# SVG → PDF conversion
# -------------------------------
.PHONY: svgs
svgs: $(PDF_SVGS)

$(RESDIR)/%.pdf: $(RESDIR)/%.svg
	$(INKSCAPE) $< --export-type=pdf --export-filename=$@

# -------------------------------
# LaTeX build
# -------------------------------

# Normal slides with overlays and notes
$(BUILDDIR)/$(MAIN).pdf: $(MAIN).tex | $(BUILDDIR)
	$(LATEXMK) -pdf -outdir=$(BUILDDIR) -shell-escape $(MAIN).tex

# Handout slides (final overlay only, with notes)
$(BUILDDIR)/$(MAIN)-handout.pdf: $(MAIN).tex | $(BUILDDIR)
	$(LATEXMK) -pdf -outdir=$(BUILDDIR) -shell-escape \
	  -jobname=$(MAIN)-handout \
	  -pdflatex="pdflatex %O '\def\HANDOUTMODE{}\input{%S}'" \
	  $(MAIN).tex

# -------------------------------
# Cleaning
# -------------------------------
.PHONY: clean
clean:
	$(LATEXMK) -C -outdir=$(BUILDDIR)
	@find . -type f -name '*.bak*' -delete
	@find . -type f -name '*.new' -delete
	@find . -type f -name 'indent.log' -delete

.PHONY: distclean
distclean: clean
	rm -rf $(BUILDDIR)

# -------------------------------
# Formatting with latexindent
# -------------------------------
.PHONY: format
format:
	latexindent -w $(MAIN).tex
	latexindent -w section/*.tex

# -------------------------------
# PDF compression
# -------------------------------
.PHONY: compress
compress: $(BUILDDIR)/$(MAIN).pdf
	gs -sDEVICE=pdfwrite -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH \
	   -sOutputFile=$(BUILDDIR)/$(MAIN)_compressed.pdf $<

# -------------------------------
# Spellcheck
# -------------------------------

.PHONY: spellcheck
spellcheck:
	@$(foreach FILE,$(TEX_FILES), $(SPELLCHECK) --mode=tex -d $(SPELLCHECK_LANG) --personal=$(SPELLCHECK_CUSTOM_DICT) -c "$(FILE)";)
