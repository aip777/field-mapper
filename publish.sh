#!/bin/bash
set -e

echo "========================================="
echo "Publishing field-mapper to PyPI"
echo "========================================="

echo "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info
find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete

echo "Building distribution packages..."
python -m build

echo "Checking distribution..."
twine check dist/*

echo ""
echo "========================================="
echo "Ready to upload!"
echo "========================================="
echo ""
echo "Choose upload destination:"
echo "1) Test PyPI (recommended first)"
echo "2) Production PyPI"
echo "3) Both (Test PyPI first, then Production)"
echo "4) Cancel"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo "Uploading to Test PyPI..."
        twine upload --repository testpypi dist/*
        echo ""
        echo "✅ Uploaded to Test PyPI!"
        echo "View at: https://test.pypi.org/project/field-mapper/"
        ;;
    2)
        echo "Uploading to Production PyPI..."
        twine upload dist/*
        echo ""
        echo "✅ Uploaded to Production PyPI!"
        echo "View at: https://pypi.org/project/field-mapper/"
        ;;
    3)
        echo "Uploading to Test PyPI first..."
        twine upload --repository testpypi dist/*
        echo ""
        echo "✅ Uploaded to Test PyPI!"
        echo ""
        read -p "Continue to Production PyPI? (y/n) " confirm
        if [[ $confirm =~ ^[Yy]$ ]]; then
            echo "Uploading to Production PyPI..."
            twine upload dist/*
            echo ""
            echo "✅ Uploaded to Production PyPI!"
            echo "View at: https://pypi.org/project/field-mapper/"
        fi
        ;;
    4)
        echo "Upload cancelled."
        exit 0
        ;;
    *)
        echo "Invalid choice. Upload cancelled."
        exit 1
        ;;
esac

echo ""
echo "========================================="
echo "Done!"
echo "========================================="