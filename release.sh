#!/bin/bash

# Release checklist:
# * update HISTORY.rst
# * tag release
# run release.sh

python3 setup.py bdist bdist_wheel
twine upload --skip-existing dist/*
