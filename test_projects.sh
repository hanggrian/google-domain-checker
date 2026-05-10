#!/bin/bash

RED="$(tput setaf 1)" && readonly RED
GREEN="$(tput setaf 2)" && readonly GREEN
YELLOW="$(tput setaf 3)" && readonly YELLOW
END="$(tput sgr0)" && readonly END

warn() { echo "$YELLOW$*$END"; } >&2
die() { echo; echo "$RED$*$END"; echo; exit 1; } >&2

SOURCE_ROOT="$(cd "$(dirname "$0")" && pwd)" && readonly SOURCE_ROOT
APPLICATION="$(cd "$SOURCE_ROOT/application" && pwd)" && readonly APPLICATION
LIBRARY="$(cd "$SOURCE_ROOT/library" && pwd)" && readonly LIBRARY
NOTEBOOK="$(cd "$SOURCE_ROOT/notebook" && pwd)" && readonly NOTEBOOK

install() {
  uv -q sync
  uv -q pip install -r website/requirements.txt
}

lint() {
  uv run pylint "$@"
  uv run stylebook .github/ *.toml
}

test() {
  if [[ $# -eq 1 ]]; then
    uv run pytest -q "$@" --cov
  else
    uv run pytest -q "$1" --cov="$1"
    shift
    for arg in "$@"; do
      uv run pytest -q "$arg" --cov="$arg" --cov-append
    done
  fi
  uv run coverage xml
}

build_docs() {
  uv run pdoc -o build/pdoc/ "$@"
}

build_website() {
  cd 'website' || exit 1
  uv run mkdocs -q build
}

COVERAGE_FILE='coverage.xml' && readonly COVERAGE_FILE
PDOC_DIR='build/pdoc/' && readonly PDOC_DIR
MKDOCS_DIR='website/site/' && readonly MKDOCS_DIR

warn 'Testing application...'

echo '(1/3) Running UV commands'
cd "$APPLICATION" || exit 1
install
lint src/
test tests/
build_website
cd "$APPLICATION" || exit 1

echo '(2/3) Checking coverage file'
if [[ ! -e "$COVERAGE_FILE" ]]; then
  die 'Coverage not found.'
fi

echo '(3/3) Checking website directory'
if [[ ! -e "$MKDOCS_DIR" ]]; then
  die 'Website not built.'
fi

warn 'Testing library...'

echo '(1/4) Running UV commands'
cd "$LIBRARY" || exit 1
install
# duplicate directory names, `uv run pylint library` wouldn't work
lint library/library/ library/tests/ library-extension/
test library/ library-extension/
build_docs library/library/ library-extension/library_extension/
build_website
cd "$LIBRARY" || exit 1

echo '(2/4) Checking coverage file'
if [[ ! -e "$COVERAGE_FILE" ]]; then
  die 'Coverage not found.'
fi

echo '(3/4) Checking documentation directory'
if [[ ! -e "$PDOC_DIR" ]]; then
  die 'Documentation not built.'
fi

echo '(4/4) Checking website directory'
if [[ ! -e "$MKDOCS_DIR" ]]; then
  die 'Website not built.'
fi

warn 'Testing notebook...'

echo '(1/3) Running UV commands'
cd "$NOTEBOOK" || exit 1
install
lint ./*.py
build_docs ./*.py
build_website
cd "$NOTEBOOK" || exit 1

echo '(2/3) Checking documentation directory'
if [[ ! -e "$PDOC_DIR" ]]; then
  die 'Documentation not built.'
fi

echo '(3/3) Checking website directory'
if [[ ! -e "$MKDOCS_DIR" ]]; then
  die 'Website not built.'
fi

echo "${GREEN}Tests complete.$END"
echo
echo 'Goodbye!'
