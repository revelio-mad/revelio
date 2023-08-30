#!/bin/bash

PYTHON_VERSIONS=("3.8" "3.9" "3.10")

# Install Python versions using pyenv
for version in "${PYTHON_VERSIONS[@]}"
do
    pyenv install $version
done
pyenv global ${PYTHON_VERSIONS[@]}
