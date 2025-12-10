#!/bin/bash

# Test runner script for Field Mapper library
# Runs all unit tests and displays summary

set -e

PROJECT_ROOT="/home/aip/PycharmProjects/field-mapper"
export PYTHONPATH="$PROJECT_ROOT"

echo "======================================================================"
echo "Running Field Mapper Unit Tests"
echo "======================================================================"
python -m unittest field_mapper/test/test_field_mapper.py -v
echo ""

echo "======================================================================"
echo "All tests completed successfully!"
echo "======================================================================"


# python -m unittest field_mapper/test/test_field_mapper.py -v
# python -m unittest field_mapper.test.test_field_mapper.TestBasicValidation -v
# python -m unittest field_mapper.test.test_field_mapper.TestBasicValidation.test_valid_data_with_all_fields -v
