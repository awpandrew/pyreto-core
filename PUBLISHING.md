# Pyreto Publishing Guide

## Preparing for PyPI Release

### 1. Ensure all changes are committed

```bash
git status
git add .
git commit -m "Release v0.5.0: Add Monte Carlo simulation engine"
```

### 2. Build the package

```bash
# Make sure build dependencies are installed
pip install --upgrade build setuptools wheel

# Build the package
python -m build

# This creates:
# - dist/pyreto-0.5.0-py3-none-any.whl
# - dist/pyreto-0.5.0.tar.gz
```

### 3. Test the build locally

```bash
# Install from the built wheel
pip install dist/pyreto-0.5.0-py3-none-any.whl

# Test import
python -c "import pyreto as pr; print(pr.__version__)"

# Test MC module
python -c "from pyreto import mc; print('MC module imported successfully')"

# Run quick tests
python test_quick.py
```

### 4. Upload to Test PyPI (optional but recommended)

```bash
# Install twine
pip install twine

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# You'll be prompted for:
# - Username: __token__
# - Password: <your-test-pypi-api-token>

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pyreto==0.5.0
```

### 5. Upload to Production PyPI

```bash
# Upload to PyPI (production)
twine upload dist/*

# You'll be prompted for:
# - Username: __token__
# - Password: <your-pypi-api-token>

# Verify installation
pip install pyreto==0.5.0
python -c "import pyreto as pr; print(f'Pyreto v{pr.__version__} installed successfully')"
python -c "from pyreto import mc; print('MC module available')"
```

## PyPI API Token Setup

If you don't have a PyPI API token:

1. Go to https://pypi.org/manage/account/
2. Scroll to "API tokens" section
3. Click "Add API token"
4. Choose scope: "Entire account" or specific project
5. Copy the token (starts with "pypi-")
6. Use it as password when prompted by twine

## Pre-flight Checklist

Before publishing, ensure:

- [ ] Version bumped in `pyproject.toml` and `src/pyreto/__init__.py`
- [ ] Description updated in `pyproject.toml`
- [ ] All tests pass
- [ ] README updated with new features
- [ ] CHANGELOG updated (if exists)
- [ ] Build succeeds without errors
- [ ] Test installation from wheel works
- [ ] MC module imports correctly
- [ ] Quick test passes

## Troubleshooting

### Build fails
```bash
# Clean build directory
rm -rf dist/ build/ *.egg-info

# Rebuild
python -m build
```

### Upload fails
```bash
# Check token is correct
# Ensure token has proper scope
# Try uploading with --verbose flag
```

### Installation fails
```bash
# Check dependencies are available
pip install numpy scipy polars
```

## Post-Publishing

After successful upload:

1. Verify on https://pypi.org/project/pyreto/
2. Check that version 0.5.0 is visible
3. Test installation in fresh virtual environment
4. Update GitHub releases if applicable
5. Announce in relevant channels

## Manual Installation from Source

If PyPI upload is not possible, users can install from source:

```bash
git clone <repository-url>
cd pyreto
git checkout mc-core
pip install -e .
```
