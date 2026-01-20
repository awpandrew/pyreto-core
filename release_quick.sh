#!/bin/bash
# Quick release script for pyreto v0.4.0
# Usage: ./release_quick.sh [test|prod]
#   test - Upload to Test PyPI only
#   prod - Upload to Production PyPI only

set -e

echo "=========================================="
echo "Pyreto Quick Release v0.4.0"
echo "=========================================="

# Check virtual environment
VENV_PYTHON=".venv/bin/python"
VENV_PIP=".venv/bin/pip"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: Virtual environment not found at .venv/"
    echo "Please run: source .venv/bin/activate"
    exit 1
fi

# Use first argument to determine target
TARGET=${1:-"test"}

echo "Target: $TARGET"

# Install build dependencies
echo "Installing build dependencies..."
$VENV_PIP install --upgrade build twine setuptools wheel

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Build the package
echo "Building package..."
$VENV_PYTHON -m build

echo "Build completed!"
ls -lh dist/

# Upload based on target
if [ "$TARGET" = "test" ]; then
    echo "Uploading to Test PyPI..."
    twine upload --repository testpypi dist/*
    echo "✓ Uploaded to Test PyPI: https://test.pypi.org/project/pyreto/"
elif [ "$TARGET" = "prod" ]; then
    echo "Uploading to Production PyPI..."
    twine upload dist/*
    echo "✓ Uploaded to Production PyPI: https://pypi.org/project/pyreto/"
else
    echo "Error: Unknown target '$TARGET'"
    echo "Usage: ./release_quick.sh [test|prod]"
    exit 1
fi

echo ""
echo "Release completed!"
