# Python Starters

![Logo](https://github.com/hanggrian/python-starters/raw/assets/logo.png)

Common Python project templates, separated by target platform and kind of
distribution.

| | Testing | Publishing | Website | Coverage
--- | :---: | :---: | :---: | :---:
application | [Pytest] | &cross; | [Material] | &check;
library | [Pytest] | [Package Index] | [Pdoc], [Material] | &check;
notebook | &cross; | &cross; | [Pdoc], [Material] | &cross;

## Frameworks

- Built-in `unittest` testing framework with [`unittest.mock`](https://docs.python.org/3/library/unittest.mock.html) suite and [pytest](https://docs.pytest.org/en/stable/) as a test
  runner.
- [Pylint](https://pylint.pycqa.org/en/stable/index.html) code linter with
  third-party ruleset [Rulebook](https://github.com/hendraanggrian/rulebook/).
- [Coverage plugin](https://github.com/pytest-dev/pytest-cov) for Pytest.

## Project layout

- Root directory:
  - GitHub [README](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes/),
    [LICENSE](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository/),
    and [gitignore](https://docs.github.com/en/get-started/getting-started-with-git/ignoring-files/)
    file.
  - [EditorConfig](https://editorconfig.org/) enforces IDE settings.
- [GitHub Actions](https://docs.github.com/en/actions/) workflows:
  - Run tests, linters and push coverage to [Codecov](https://codecov.io/).
  - Activate [Renovate](https://docs.renovatebot.com/) bot to alert out-of-date
    dependencies.
- [UV](https://docs.astral.sh/uv/) package manager:
  - `pyproject.toml` with hatchling build system.
  - `uv.lock` for deterministic dependencies.
- Website module:
  - [MkDocs](https://www.mkdocs.org/) for generating webpages displaying README
    and other content.
  - The webpages are manually deployed with `mkdocs gh-deploy`.

[Pytest]: https://docs.pytest.org/en/stable/
[Package Index]: https://pypi.org/
[Pdoc]: https://pdoc.dev/
[Material]: https://squidfunk.github.io/mkdocs-material/
