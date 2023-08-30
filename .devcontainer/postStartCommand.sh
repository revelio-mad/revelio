#!/bin/bash

PYTORCH_INDEX_URL=https://download.pytorch.org/whl/cu118

# If nvidia-smi is present and exits with code 0, we assume the container has GPU capabilities
# and download PyTorch with CUDA support; otherwise, we fall back to CPU-only PyTorch to speed up download times.
if nvidia-smi >/dev/null 2>&1; then
    pip install -r requirements-dev.txt --extra-index-url $PYTORCH_INDEX_URL
    pip install -e . --extra-index-url $PYTORCH_INDEX_URL
else
    pip install -r requirements-dev.txt
    pip install -e .
fi

pipx install tox

npm install
pre-commit install --install-hooks
pre-commit install -t commit-msg --install-hooks
