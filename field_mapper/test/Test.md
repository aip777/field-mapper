# Field Mapper Test Suite

### 1. `test_field_mapper.py` (Comprehensive Tests - 42 tests)

#### TestBasicValidation (6 tests)
- Valid data with all fields
- Missing required field detection
- Invalid type detection
- Max length validation for strings
- Max length validation for lists
- Max length validation for dicts

#### TestOptionalFields (6 tests)
- Optional fields can be missing
- Optional values can be empty
- Zero (0) is a valid value (not empty)
- False is a valid value (not empty)
- Required value missing detection
- Required field/value combinations

#### TestCustomValidators (4 tests)
- Boolean return validators (valid cases)
- Boolean return validators (invalid cases)
- Exception raising validators
- Complex multi-check validators

#### TestNestedDataExtraction (6 tests)
- Extract from array by index (email[0])
- Extract from nested dict (phone.mobile)
- Extract from nested array of dicts (salary[0].amount)
- Extract from all array items (skills[].name)
- Custom validators with nested data
- Type validation checks source structure

#### TestComplexTypes (4 tests)
- List type validation
- Dict type validation
- Empty lists allowed (when required_value: False)
- Empty dicts allowed (when required_value: False)

#### TestDuplicateDetection (3 tests)
- No duplicates processing
- Duplicate detection and error raising
- Skip duplicate flag behavior

#### TestErrorHandling (5 tests)
- Error list populated on validation failure
- Error message format and content
- Multiple validation errors captured
- Error accumulation between runs
- Invalid input type handling

#### TestFieldMapping (2 tests)
- Simple field name mapping
- Field mapping with same source/target names

#### TestEmptyValueHandling (8 tests)
- None is considered empty
- Empty string ("") is considered empty
- Empty list ([]) is considered empty
- Empty dict ({}) is considered empty
- Zero (0) is NOT considered empty
- False is NOT considered empty
- String with spaces is NOT considered empty
- Empty value validation with required_value

## Running Tests

### Run all tests:
```bash
./run_tests.sh
```

### Run specific test file:
```bash
# Comprehensive tests
PYTHONPATH=. python -m unittest field_mapper/test/test_field_mapper.py -v
```

### Run specific test class:
```bash
PYTHONPATH=. python -m unittest field_mapper.test.test_field_mapper.TestBasicValidation -v
```

### Run specific test method:
```bash
PYTHONPATH=. python -m unittest field_mapper.test.test_field_mapper.TestBasicValidation.test_valid_data_with_all_fields -v
```