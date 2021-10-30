#!/bin/bash

# Create a virtual environment
pwd=${PWD##*/}
python3 -m venv venv_$pwd

# Activate the virtual environment
source venv_$pwd/bin/activate

# Install the dev packages
pip install --upgrade pip setuptools
pip install -r requirements-dev.txt

# Install the pre-commit hook
pre-commit install
