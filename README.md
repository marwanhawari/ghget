<p align="center">
  <img width=60% height=auto src="https://github.com/marwanhawari/ghget/raw/main/docs/ghget_logo.png" alt="ghget logo"/>
  
</p>

[![PyPI version](https://badge.fury.io/py/ghget.svg)](https://badge.fury.io/py/ghget)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/ghget)](https://pypi.org/project/ghget/)
[![Build Status](https://github.com/marwanhawari/ghget/actions/workflows/build.yml/badge.svg)](https://github.com/marwanhawari/ghget/actions)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](https://github.com/marwanhawari/ghget/blob/main/CODE_OF_CONDUCT.md)
[![GitHub](https://img.shields.io/github/license/marwanhawari/ghget?color=blue)](https://github.com/marwanhawari/ghget/blob/main/LICENSE)

# Description
Download single files or directories from a GitHub repository without cloning its entire contents.

# Features
* No need to manually create a raw GitHub url for individual files, just provide the web url.
* Recursively download entire directories.
* Download from private repos by setting a `GITHUB_TOKEN` environment variable.
* Lightweight, easy to install, and easy to use.

# Installation
The `ghget` package can be installed directly using `pip`.
```
pip install ghget
```

# Usage
* Easily download single files given the GitHub url:
```
$ ghget https://github.com/naiquevin/pipdeptree/blob/master/pipdeptree.py
Downloading pipdeptree.py file...
Done!
```

* Recursively download a specific directory from a GitHub repo: 
```
$ ghget https://github.com/pandas-dev/pandas/tree/master/scripts
Downloading scripts directory...
Done!

$ tree
.
└── scripts
    ├── __init__.py
    ├── generate_pip_deps_from_conda.py
    ├── list_future_warnings.sh
    ├── no_bool_in_generic.py
    ├── pandas_errors_documented.py
    ├── sync_flake8_versions.py
    ├── tests
    │   ├── __init__.py
    │   ├── conftest.py
    │   ├── test_no_bool_in_generic.py
    │   ├── test_sync_flake8_versions.py
    │   ├── test_use_pd_array_in_core.py
    │   └── test_validate_docstrings.py
    ├── use_pd_array_in_core.py
    ├── validate_docstrings.py
    └── validate_rst_title_capitalization.py

```


### Options
```
usage: ghget [-h] url

positional arguments:
  url         The url for the file or directory you want to download.

optional arguments:
  -h, --help  show this help message and exit
```
