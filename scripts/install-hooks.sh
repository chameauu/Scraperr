#!/usr/bin/env sh
set -eu

# Install pre-commit hooks into .git/hooks
uv run pre-commit install

echo "pre-commit hooks installed."
