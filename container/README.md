# Use container to build LaTeX project

Mount the project directory inside a temporary container and build a `.pdf`.
Requires no program to be installed but a long time for the first optimized image build.
Assumes:

- that in the current directory everything is contained
- there is a `main.tex` file in that directory

## Run

```sh
# Build Image with tag 'latex-full'
#       using the 'Containerfile' in this directory
docker build -t latex-full .
# Run with default argument that compiles 'main.tex' to build
docker run --rm -v $(pwd):/data latex-full
# Windows:
docker run --rm -v ${PWD}:/data latex-full
```

Alternatively use `podman` instead of `docker`.

### Optional

This container contains `gs` to compress e.g. images in a `.pdf` file:

```sh
docker run --rm -v $(pwd):/data latex-full gs -o compressed.pdf -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress -dNOPAUSE -dBATCH -dQUIET build/main.pdf
```
