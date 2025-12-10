#!/bin/bash

# Script to run all Field Mapper examples
# Usage: ./run_all_examples.sh

set -e  # Exit on error

PROJECT_ROOT="/home/aip/PycharmProjects/field-mapper"
export PYTHONPATH="$PROJECT_ROOT"

echo "======================================================================"
echo "Running Field Mapper Examples"
echo "======================================================================"
echo ""

# Success Cases
echo "══════════════════════════════════════════════════════════════════════"
echo "SUCCESS CASES"
echo "══════════════════════════════════════════════════════════════════════"
echo ""

echo "Running 01_basic_validation.py..."
python "$PROJECT_ROOT/field_mapper/examples/success_cases/01_basic_validation.py"
echo ""

echo "Running 02_custom_validation.py..."
python "$PROJECT_ROOT/field_mapper/examples/success_cases/02_custom_validation.py"
echo ""

echo "Running 03_nested_data_extraction.py..."
python "$PROJECT_ROOT/field_mapper/examples/success_cases/03_nested_data_extraction.py"
echo ""

echo "Running 04_optional_fields.py..."
python "$PROJECT_ROOT/field_mapper/examples/success_cases/04_optional_fields.py"
echo ""

echo "Running 05_complex_types.py..."
python "$PROJECT_ROOT/field_mapper/examples/success_cases/05_complex_types.py"
echo ""

# Error Cases
echo "══════════════════════════════════════════════════════════════════════"
echo "ERROR CASES"
echo "══════════════════════════════════════════════════════════════════════"
echo ""

echo "Running 01_missing_required_fields.py..."
python "$PROJECT_ROOT/field_mapper/examples/error_cases/01_missing_required_fields.py"
echo ""

echo "Running 02_invalid_types.py..."
python "$PROJECT_ROOT/field_mapper/examples/error_cases/02_invalid_types.py"
echo ""

echo "Running 03_max_length_exceeded.py..."
python "$PROJECT_ROOT/field_mapper/examples/error_cases/03_max_length_exceeded.py"
echo ""

echo "Running 04_custom_validation_failures.py..."
python "$PROJECT_ROOT/field_mapper/examples/error_cases/04_custom_validation_failures.py"
echo ""

echo "Running 05_required_value_missing.py..."
python "$PROJECT_ROOT/field_mapper/examples/error_cases/05_required_value_missing.py"
echo ""

echo "Running 06_duplicate_data.py..."
python "$PROJECT_ROOT/field_mapper/examples/error_cases/06_duplicate_data.py"
echo ""

echo "Running 07_nested_data_validation_errors.py..."
python "$PROJECT_ROOT/field_mapper/examples/error_cases/07_nested_data_validation_errors.py"
echo ""

echo "======================================================================"
echo "All examples completed!"
echo "======================================================================"