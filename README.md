[![GitHub Actions](https://img.shields.io/github/actions/workflow/status/hanggrian/google-domain-checker/code-analysis.yaml)](https://github.com/hanggrian/google-domain-checker/actions/workflows/code-analysis.yaml)
[![Codecov](https://img.shields.io/codecov/c/gh/hanggrian/google-domain-checker)](https://app.codecov.io/gh/hanggrian/google-domain-checker/)
[![Renovate](https://img.shields.io/badge/dependency-mend-blue)](https://developer.mend.io/github/hanggrian/google-domain-checker/)
[![Python](https://img.shields.io/badge/python-3.10+-informational)](https://docs.python.org/3.10/)

# Google Domain Checker

Python script to check if email addresses are from Google Domain in batch.

## Usage

### Check

Check individual email addresses in a single thread.

```sh
uv run check email1@domain.com email2@domain.com
```

### Convert

Multi-threaded reading of email column in CSV and append result on a new column.

```sh
uv run convert file.csv
```
