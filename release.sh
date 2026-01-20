#!/bin/bash
# Pyreto Release Script for v0.4.0
# This script builds and publishes pyreto to PyPI

set -e

echo "=========================================="
echo "Pyreto Release Script v0.4.0"
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

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python --version

# Step 1: Install build dependencies
echo -e "${YELLOW}Installing build dependencies...${NC}"
pip install --upgrade build twine setuptools wheel

# Step 2: Clean previous builds
echo -e "${YELLOW}Cleaning previous builds...${NC}"
rm -rf dist/ build/ *.egg-info/

# Step 3: Run tests
echo -e "${YELLOW}Running tests...${NC}"
python test_quick.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Tests failed. Aborting release.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Tests passed${NC}"

# Step 4: Build the package
echo -e "${YELLOW}Building package...${NC}"
python -m build

echo -e "${GREEN}✓ Build completed${NC}"

# Step 5: Check the built package
echo -e "${YELLOW}Checking built packages...${NC}"
ls -lh dist/

# Step 6: Upload to Test PyPI (optional)
echo -e "${YELLOW}Upload to Test PyPI? (y/n)${NC}"
read -r upload_test
if [ "$upload_test" = "y" ]; then
    echo -e "${YELLOW}Uploading to Test PyPI...${NC}"
    twine upload --repository testpypi dist/*
    echo -e "${GREEN}✓ Uploaded to Test PyPI${NC}"
    
    echo -e "${YELLOW}Test installation from Test PyPI? (y/n)${NC}"
    read -r test_install
    if [ "$test_install" = "y" ]; then
        echo -e "${YELLOW}Testing installation...${NC}"
        pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pyreto==0.4.0
        python -c "import pyreto as pr; print(f'Installed version: {pr.__version__}')"
        python -c "from pyreto import mc; print('MC module available')"
    fi
fi

# Step 7: Upload to Production PyPI
echo -e "${YELLOW}Upload to Production PyPI? (y/n)${NC}"
echo -e "${RED}WARNING: This will make the release public!${NC}"
read -r upload_prod
if [ "$upload_prod" = "y" ]; then
    echo -e "${YELLOW}Uploading to Production PyPI...${NC}"
    twine upload dist/*
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
