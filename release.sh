#!/bin/bash
# Pyreto Release Script for v0.5.0
# This script builds and publishes pyreto to PyPI

set -e

echo "=========================================="
echo "Pyreto Release Script v0.5.0"
echo "=========================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}Error: pyproject.toml not found. Are you in the pyreto root directory?${NC}"
    exit 1
fi

# Detect virtual environment
VENV_PYTHON=".venv/bin/python"
VENV_PIP=".venv/bin/pip"

if [ ! -f "$VENV_PYTHON" ]; then
    echo -e "${RED}Error: Virtual environment not found at .venv/${NC}"
    echo -e "${YELLOW}Please create and activate a virtual environment first:${NC}"
    echo -e "${YELLOW}  python -m venv .venv${NC}"
    echo -e "${YELLOW}  source .venv/bin/activate${NC}"
    echo -e "${YELLOW}  pip install -e .${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Virtual environment detected${NC}"
echo -e "${GREEN}✓ Using Python: $VENV_PYTHON${NC}"

# Check for PyPI API key in environment
if [ -n "$PYPI_PYRETO_API" ]; then
    echo -e "${GREEN}✓ PyPI API key found in PYPI_PYRETO_API environment variable${NC}"
    export TWINE_USERNAME="__token__"
    export TWINE_PASSWORD="$PYPI_PYRETO_API"
else
    echo -e "${YELLOW}⚠ No PYPI_PYRETO_API environment variable found${NC}"
    echo -e "${YELLOW}You will be prompted for credentials during upload${NC}"
fi

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
$VENV_PYTHON --version

# Install pip if not present
if [ ! -f "$VENV_PIP" ]; then
    echo -e "${YELLOW}Installing pip in virtual environment...${NC}"
    $VENV_PYTHON -m ensurepip --upgrade
    $VENV_PYTHON -m pip install --upgrade pip
    VENV_PIP=".venv/bin/pip"
fi

# Step 1: Install build dependencies
echo -e "${YELLOW}Installing build dependencies...${NC}"
$VENV_PIP install --upgrade build twine setuptools wheel

# Step 2: Clean previous builds
echo -e "${YELLOW}Cleaning previous builds...${NC}"
rm -rf dist/ build/ *.egg-info/

# Step 3: Run in-project tests
echo -e "${YELLOW}Running in-project tests...${NC}"
cd /home/aisandy/Documents/pyreto-lib
source .venv/bin/activate
python test_quick.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Tests failed. Aborting release.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Tests passed${NC}"

# Step 4: Build the package
echo -e "${YELLOW}Building package...${NC}"
$VENV_PYTHON -m build

echo -e "${GREEN}✓ Build completed${NC}"

# Step 5: Check the built package
echo -e "${YELLOW}Checking built packages...${NC}"
ls -lh dist/

# Step 6: Verify the package
echo -e "${YELLOW}Verifying package...${NC}"
$VENV_PIP install dist/pyreto-0.5.0-py3-none-any.whl
$VENV_PYTHON -c "import pyreto as pr; print(f'Package version: {pr.__version__}')"
$VENV_PYTHON -c "from pyreto import mc; print('MC module imported successfully')"

# Step 7: Upload to Test PyPI (optional)
echo -e "${YELLOW}Upload to Test PyPI? (y/n)${NC}"
read -r upload_test
if [ "$upload_test" = "y" ]; then
    echo -e "${YELLOW}Uploading to Test PyPI...${NC}"
    if [ -n "$PYPI_PYRETO_API" ]; then
        twine upload --repository testpypi dist/*
    else
        twine upload --repository testpypi dist/*
    fi
    echo -e "${GREEN}✓ Uploaded to Test PyPI${NC}"
    
    echo -e "${YELLOW}Test installation from Test PyPI? (y/n)${NC}"
    read -r test_install
    if [ "$test_install" = "y" ]; then
        echo -e "${YELLOW}Testing installation...${NC}"
        $VENV_PIP install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pyreto==0.5.0
        $VENV_PYTHON -c "import pyreto as pr; print(f'Installed version: {pr.__version__}')"
        $VENV_PYTHON -c "from pyreto import mc; print('MC module available')"
    fi
fi

# Step 8: Upload to Production PyPI
echo -e "${YELLOW}Upload to Production PyPI? (y/n)${NC}"
echo -e "${RED}WARNING: This will make the release public!${NC}"
read -r upload_prod
if [ "$upload_prod" = "y" ]; then
    echo -e "${YELLOW}Uploading to Production PyPI...${NC}"
    if [ -n "$PYPI_PYRETO_API" ]; then
        twine upload dist/*
    else
        twine upload dist/*
    fi
    echo -e "${GREEN}✓ Uploaded to Production PyPI${NC}"
    
    echo -e "${GREEN}✓ Release completed successfully!${NC}"
    echo -e "${YELLOW}Verify at: https://pypi.org/project/pyreto/${NC}"
else
    echo -e "${YELLOW}Build artifacts saved in dist/ for manual upload${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Release script finished${NC}"
echo -e "${GREEN}========================================${NC}"
