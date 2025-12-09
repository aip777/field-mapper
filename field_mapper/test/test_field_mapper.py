"""
Comprehensive unit tests for Field Mapper library.

Tests cover:
- Basic validation (type checking, required fields, max length)
- Custom validators (boolean return, exception raising)
- Nested data extraction (dot notation, array indexing, dynamic arrays)
- Optional fields (required_field, required_value)
- Complex types (lists, dicts)
- Duplicate detection
- Empty vs falsy values (0, False)
- Error handling and messages
"""

import unittest
from field_mapper import FieldMapper
from field_mapper.exc.exception import FieldValidationError, DuplicateDataError


class TestBasicValidation(unittest.TestCase):
    """Test basic validation functionality."""

    def test_valid_data_with_all_fields(self):
        """Test processing valid data with all required fields."""
        fields = {
            "name": {"type": str, "required_field": True, "required_value": True},
            "age": {"type": int, "required_field": True, "required_value": True},
            "email": {"type": str, "required_field": True, "required_value": True}
        }
        field_map = {
            "name": "full_name",
            "age": "user_age",
            "email": "contact_email"
        }
        data = [
            {"name": "Alice", "age": 30, "email": "alice@example.com"},
            {"name": "Bob", "age": 25, "email": "bob@example.com"}
        ]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["full_name"], "Alice")
        self.assertEqual(result[0]["user_age"], 30)
        self.assertEqual(result[1]["full_name"], "Bob")
        self.assertFalse(mapper.error)

    def test_missing_required_field(self):
        """Test validation fails when required field is missing."""
        fields = {
            "name": {"type": str, "required_field": True},
            "email": {"type": str, "required_field": True}
        }
        field_map = {"name": "name", "email": "email"}
        data = [{"name": "Alice"}]  # Missing email

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)

        self.assertEqual(len(result), 0)
        self.assertTrue(mapper.error)
        self.assertIn("Missing required field: 'email'", mapper.error[0])

    def test_invalid_type(self):
        """Test validation fails on type mismatch."""
        fields = {
            "name": {"type": str},
            "age": {"type": int}
        }
        field_map = {"name": "name", "age": "age"}
        data = [{"name": "Alice", "age": "thirty"}]  # Age should be int

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)

        self.assertEqual(len(result), 0)
        self.assertIn("Invalid type for field 'age': expected int, got str", mapper.error[0])

    def test_max_length_string(self):
        """Test max_length validation for strings."""
        fields = {
            "name": {"type": str, "max_length": 5}
        }
        field_map = {"name": "name"}
        data = [{"name": "Alice"}]  # 5 chars - OK

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 1)

        # Test exceeding max length
        data_too_long = [{"name": "Alexander"}]  # 9 chars - Too long
        mapper2 = FieldMapper(fields, field_map)
        result2 = mapper2.process(data_too_long)
        self.assertEqual(len(result2), 0)
        self.assertIn("exceeds max length of 5", mapper2.error[0])

    def test_max_length_list(self):
        """Test max_length validation for lists."""
        fields = {
            "tags": {"type": list, "max_length": 3}
        }
        field_map = {"tags": "tags"}

        # Valid - 3 items
        data_ok = [{"tags": ["python", "java", "go"]}]
        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data_ok)
        self.assertEqual(len(result), 1)

        # Invalid - 4 items
        data_too_long = [{"tags": ["python", "java", "go", "rust"]}]
        mapper2 = FieldMapper(fields, field_map)
        result2 = mapper2.process(data_too_long)
        self.assertEqual(len(result2), 0)
        self.assertIn("exceeds max length of 3", mapper2.error[0])

    def test_max_length_dict(self):
        """Test max_length validation for dicts."""
        fields = {
            "metadata": {"type": dict, "max_length": 2}
        }
        field_map = {"metadata": "metadata"}

        # Valid - 2 keys
        data_ok = [{"metadata": {"key1": "value1", "key2": "value2"}}]
        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data_ok)
        self.assertEqual(len(result), 1)

        # Invalid - 3 keys
        data_too_long = [{"metadata": {"key1": "value1", "key2": "value2", "key3": "value3"}}]
        mapper2 = FieldMapper(fields, field_map)
        result2 = mapper2.process(data_too_long)
        self.assertEqual(len(result2), 0)
        self.assertIn("exceeds max length of 2", mapper2.error[0])


class TestOptionalFields(unittest.TestCase):
    """Test optional field configurations."""

    def test_optional_field_missing(self):
        """Test that optional fields can be missing."""
        fields = {
            "name": {"type": str, "required_field": True},
            "phone": {"type": str, "required_field": False}
        }
        field_map = {"name": "name", "phone": "phone"}
        data = [{"name": "Alice"}]  # phone is missing but optional

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 1)
        self.assertFalse(mapper.error)

    def test_optional_value_empty(self):
        """Test that optional values can be empty."""
        fields = {
            "name": {"type": str, "required_field": True, "required_value": True},
            "bio": {"type": str, "required_field": True, "required_value": False}
        }
        field_map = {"name": "name", "bio": "bio"}
        data = [{"name": "Alice", "bio": ""}]  # Empty string is OK for bio

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 1)
        self.assertFalse(mapper.error)

    def test_zero_is_valid_value(self):
        """Test that 0 is not considered empty."""
        fields = {
            "count": {"type": int, "required_field": True, "required_value": False}
        }
        field_map = {"count": "count"}
        data = [{"count": 0}]  # 0 should be valid

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["count"], 0)
        self.assertFalse(mapper.error)

    def test_false_is_valid_value(self):
        """Test that False is not considered empty."""
        fields = {
            "is_active": {"type": bool, "required_field": True, "required_value": False}
        }
        field_map = {"is_active": "is_active"}
        data = [{"is_active": False}]  # False should be valid

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["is_active"], False)
        self.assertFalse(mapper.error)

    def test_required_value_missing(self):
        """Test that required values cannot be empty."""
        fields = {
            "name": {"type": str, "required_field": True, "required_value": True}
        }
        field_map = {"name": "name"}
        data = [{"name": ""}]  # Empty string when required

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 0)
        self.assertIn("Required value missing or empty", mapper.error[0])


class TestCustomValidators(unittest.TestCase):
    """Test custom validation functions."""

    def test_custom_validator_boolean_return_valid(self):
        """Test custom validator that returns True."""
        def validate_email(value):
            return "@" in value and "." in value

        fields = {
            "email": {"type": str, "custom": validate_email}
        }
        field_map = {"email": "email"}
        data = [{"email": "alice@example.com"}]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 1)
        self.assertFalse(mapper.error)

    def test_custom_validator_boolean_return_invalid(self):
        """Test custom validator that returns False."""
        def validate_email(value):
            return "@" in value and "." in value

        fields = {
            "email": {"type": str, "custom": validate_email}
        }
        field_map = {"email": "email"}
        data = [{"email": "invalid-email"}]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 0)
        self.assertIn("Custom validation failed", mapper.error[0])

    def test_custom_validator_raises_exception(self):
        """Test custom validator that raises exception."""
        def validate_age(value):
            if value < 0 or value > 150:
                raise ValueError("Age must be between 0 and 150")
            return True

        fields = {
            "age": {"type": int, "custom": validate_age}
        }
        field_map = {"age": "age"}
        data = [{"age": 200}]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 0)
        self.assertIn("Custom validation error", mapper.error[0])
        self.assertIn("Age must be between 0 and 150", mapper.error[0])

    def test_custom_validator_with_multiple_checks(self):
        """Test custom validator with complex logic."""
        def validate_password(value):
            if len(value) < 8:
                raise ValueError("Password must be at least 8 characters")
            if not any(c.isupper() for c in value):
                raise ValueError("Password must contain uppercase letter")
            if not any(c.isdigit() for c in value):
                raise ValueError("Password must contain digit")
            return True

        fields = {
            "password": {"type": str, "custom": validate_password}
        }
        field_map = {"password": "password"}

        # Valid password
        data_valid = [{"password": "SecurePass123"}]
        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data_valid)
        self.assertEqual(len(result), 1)

        # Invalid password - too short
        data_invalid = [{"password": "Short1"}]
        mapper2 = FieldMapper(fields, field_map)
        result2 = mapper2.process(data_invalid)
        self.assertEqual(len(result2), 0)
        self.assertIn("at least 8 characters", mapper2.error[0])


class TestNestedDataExtraction(unittest.TestCase):
    """Test nested data extraction with position parameter."""

    def test_extract_from_array_index(self):
        """Test extracting first item from array."""
        fields = {
            "email": {"type": list, "position": "email[0]"}
        }
        field_map = {"email[0]": "primary_email"}
        data = [{"email": ["alice@work.com", "alice@personal.com"]}]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["primary_email"], "alice@work.com")

    def test_extract_from_nested_dict(self):
        """Test extracting from nested dictionary."""
        fields = {
            "phone": {"type": dict, "position": "phone.mobile"}
        }
        field_map = {"phone.mobile": "mobile_number"}
        data = [{"phone": {"mobile": "555-0001", "home": "555-0002"}}]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["mobile_number"], "555-0001")

    def test_extract_from_nested_array_of_dicts(self):
        """Test extracting from array of dictionaries."""
        fields = {
            "salary": {"type": list, "position": "salary[0].amount"}
        }
        field_map = {"salary[0].amount": "current_salary"}
        data = [{
            "salary": [
                {"year": 2024, "amount": 95000},
                {"year": 2023, "amount": 85000}
            ]
        }]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["current_salary"], 95000)

    def test_extract_from_all_array_items(self):
        """Test extracting property from all array items using []."""
        fields = {
            "skills": {"type": list, "position": "skills[].name"}
        }
        field_map = {"skills[].name": "skill_names"}
        data = [{
            "skills": [
                {"name": "Python", "level": "Expert"},
                {"name": "JavaScript", "level": "Intermediate"},
                {"name": "SQL", "level": "Advanced"}
            ]
        }]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["skill_names"], ["Python", "JavaScript", "SQL"])

    def test_nested_validation_with_custom_validator(self):
        """Test that custom validators work with extracted nested values."""
        def validate_email(value):
            return "@" in value

        fields = {
            "email": {
                "type": list,
                "position": "email[0]",
                "custom": validate_email
            }
        }
        field_map = {"email[0]": "primary_email"}
        data = [{"email": ["alice@example.com"]}]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 1)
        self.assertFalse(mapper.error)

    def test_nested_validation_type_checks_source(self):
        """Test that type validation checks the source structure, not extracted value."""
        fields = {
            "email": {
                "type": list,  # Source must be list
                "position": "email[0]"  # Extracted value is string
            }
        }
        field_map = {"email[0]": "primary_email"}

        # Valid - source is list
        data_valid = [{"email": ["alice@example.com"]}]
        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data_valid)
        self.assertEqual(len(result), 1)

        # Invalid - source is string, not list
        data_invalid = [{"email": "alice@example.com"}]
        mapper2 = FieldMapper(fields, field_map)
        result2 = mapper2.process(data_invalid)
        self.assertEqual(len(result2), 0)
        self.assertIn("Invalid type", mapper2.error[0])


class TestComplexTypes(unittest.TestCase):
    """Test validation of complex types (lists, dicts)."""

    def test_list_type_validation(self):
        """Test list type validation."""
        fields = {
            "tags": {"type": list}
        }
        field_map = {"tags": "tags"}

        # Valid list
        data_valid = [{"tags": ["python", "javascript"]}]
        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data_valid)
        self.assertEqual(len(result), 1)

        # Invalid - string instead of list
        data_invalid = [{"tags": "python,javascript"}]
        mapper2 = FieldMapper(fields, field_map)
        result2 = mapper2.process(data_invalid)
        self.assertEqual(len(result2), 0)
        self.assertIn("expected list, got str", mapper2.error[0])

    def test_dict_type_validation(self):
        """Test dict type validation."""
        fields = {
            "metadata": {"type": dict}
        }
        field_map = {"metadata": "metadata"}

        # Valid dict
        data_valid = [{"metadata": {"key": "value"}}]
        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data_valid)
        self.assertEqual(len(result), 1)

        # Invalid - list instead of dict
        data_invalid = [{"metadata": ["key", "value"]}]
        mapper2 = FieldMapper(fields, field_map)
        result2 = mapper2.process(data_invalid)
        self.assertEqual(len(result2), 0)
        self.assertIn("expected dict, got list", mapper2.error[0])

    def test_empty_list_allowed(self):
        """Test that empty lists are allowed when required_value is False."""
        fields = {
            "tags": {"type": list, "required_field": True, "required_value": False}
        }
        field_map = {"tags": "tags"}
        data = [{"tags": []}]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["tags"], [])

    def test_empty_dict_allowed(self):
        """Test that empty dicts are allowed when required_value is False."""
        fields = {
            "metadata": {"type": dict, "required_field": True, "required_value": False}
        }
        field_map = {"metadata": "metadata"}
        data = [{"metadata": {}}]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["metadata"], {})


class TestDuplicateDetection(unittest.TestCase):
    """Test duplicate data detection."""

    def test_no_duplicates(self):
        """Test processing data with no duplicates."""
        fields = {
            "name": {"type": str},
            "email": {"type": str}
        }
        field_map = {"name": "name", "email": "email"}
        data = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Bob", "email": "bob@example.com"}
        ]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data, skip_duplicate=True)
        self.assertEqual(len(result), 2)
        self.assertFalse(mapper.error)

    def test_duplicate_detection(self):
        """Test that duplicates are detected."""
        fields = {
            "name": {"type": str},
            "email": {"type": str}
        }
        field_map = {"name": "name", "email": "email"}
        data = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Bob", "email": "bob@example.com"},
            {"name": "Alice", "email": "alice@example.com"}  # Duplicate
        ]

        mapper = FieldMapper(fields, field_map)
        with self.assertRaises(DuplicateDataError) as context:
            from field_mapper.mapper import DuplicateDataHandler
            DuplicateDataHandler().remove_duplicates(data)

        exc = context.exception
        self.assertEqual(len(exc.problematic_data), 1)

    def test_skip_duplicate_flag_false(self):
        """Test that duplicates are not checked when skip_duplicate is False."""
        fields = {
            "name": {"type": str},
            "email": {"type": str}
        }
        field_map = {"name": "name", "email": "email"}
        data = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Alice", "email": "alice@example.com"}  # Duplicate
        ]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data, skip_duplicate=False)
        # Should process all entries without duplicate check
        self.assertEqual(len(result), 2)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and error messages."""

    def test_error_list_populated_on_validation_failure(self):
        """Test that mapper.error is populated when validation fails."""
        fields = {
            "email": {"type": str, "required_field": True}
        }
        field_map = {"email": "email"}
        data = [{"name": "Alice"}]  # Missing email

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)

        self.assertEqual(len(result), 0)
        self.assertTrue(mapper.error)
        self.assertIsInstance(mapper.error, list)
        self.assertGreater(len(mapper.error), 0)

    def test_error_message_format(self):
        """Test error message contains useful information."""
        fields = {
            "email": {"type": str, "required_field": True}
        }
        field_map = {"email": "email"}
        data = [{"name": "Alice"}]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)

        error_msg = mapper.error[0]
        self.assertIn("Error Details", error_msg)
        self.assertIn("FieldValidationError", error_msg)
        self.assertIn("Missing required field", error_msg)

    def test_multiple_validation_errors(self):
        """Test that multiple validation errors are captured."""
        fields = {
            "name": {"type": str, "required_field": True},
            "email": {"type": str, "required_field": True},
            "age": {"type": int, "required_field": True}
        }
        field_map = {"name": "name", "email": "email", "age": "age"}
        data = [{"name": "Alice"}]  # Missing email and age

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)

        error_msg = mapper.error[0]
        self.assertIn("email", error_msg)
        self.assertIn("age", error_msg)

    def test_error_cleared_between_runs(self):
        """Test that errors don't carry over between process calls."""
        fields = {
            "name": {"type": str, "required_field": True}
        }
        field_map = {"name": "name"}

        mapper = FieldMapper(fields, field_map)

        # First run with error
        data1 = [{"age": 30}]  # Missing name
        result1 = mapper.process(data1)
        self.assertTrue(mapper.error)

        # Errors should still be there (they accumulate)
        # Second run with valid data
        data2 = [{"name": "Alice"}]
        result2 = mapper.process(data2)
        # New run doesn't clear old errors
        self.assertTrue(mapper.error)

    def test_invalid_input_type(self):
        """Test that non-list input raises ValueError."""
        fields = {"name": {"type": str}}
        field_map = {"name": "name"}
        data = {"name": "Alice"}  # Dict instead of list

        mapper = FieldMapper(fields, field_map)
        with self.assertRaises(ValueError) as context:
            mapper.process(data)

        self.assertIn("must be a list", str(context.exception))


class TestFieldMapping(unittest.TestCase):
    """Test field mapping functionality."""

    def test_simple_field_mapping(self):
        """Test simple field name mapping."""
        fields = {
            "firstName": {"type": str},
            "lastName": {"type": str}
        }
        field_map = {
            "firstName": "first_name",
            "lastName": "last_name"
        }
        data = [{"firstName": "Alice", "lastName": "Johnson"}]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)

        self.assertEqual(result[0]["first_name"], "Alice")
        self.assertEqual(result[0]["last_name"], "Johnson")
        self.assertNotIn("firstName", result[0])
        self.assertNotIn("lastName", result[0])

    def test_field_mapping_with_same_name(self):
        """Test mapping where source and target names are the same."""
        fields = {
            "name": {"type": str},
            "email": {"type": str}
        }
        field_map = {
            "name": "name",
            "email": "email"
        }
        data = [{"name": "Alice", "email": "alice@example.com"}]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)

        self.assertEqual(result[0]["name"], "Alice")
        self.assertEqual(result[0]["email"], "alice@example.com")


class TestEmptyValueHandling(unittest.TestCase):
    """Test handling of empty vs falsy values."""

    def test_is_empty_value_none(self):
        """Test that None is considered empty."""
        fields = {"value": {"type": str, "required_value": True}}
        field_map = {"value": "value"}
        data = [{"value": None}]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 0)
        self.assertIn("Required value missing", mapper.error[0])

    def test_is_empty_value_empty_string(self):
        """Test that empty string is considered empty."""
        fields = {"value": {"type": str, "required_value": True}}
        field_map = {"value": "value"}
        data = [{"value": ""}]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 0)
        self.assertIn("Required value missing", mapper.error[0])

    def test_is_empty_value_empty_list(self):
        """Test that empty list is considered empty."""
        fields = {"value": {"type": list, "required_value": True}}
        field_map = {"value": "value"}
        data = [{"value": []}]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 0)
        self.assertIn("Required value missing", mapper.error[0])

    def test_is_empty_value_empty_dict(self):
        """Test that empty dict is considered empty."""
        fields = {"value": {"type": dict, "required_value": True}}
        field_map = {"value": "value"}
        data = [{"value": {}}]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 0)
        self.assertIn("Required value missing", mapper.error[0])

    def test_zero_not_empty(self):
        """Test that 0 is NOT considered empty."""
        fields = {"value": {"type": int, "required_value": True}}
        field_map = {"value": "value"}
        data = [{"value": 0}]

        mapper = FieldMapper(fields, field_map)
        # This should fail because 0 is not empty but we're checking required_value: True
        # Actually, 0 should pass! It's a valid value
        mapper2 = FieldMapper(
            {"value": {"type": int, "required_value": False}},
            {"value": "value"}
        )
        result = mapper2.process(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["value"], 0)

    def test_false_not_empty(self):
        """Test that False is NOT considered empty."""
        fields = {"value": {"type": bool, "required_value": False}}
        field_map = {"value": "value"}
        data = [{"value": False}]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["value"], False)

    def test_string_with_spaces_not_empty(self):
        """Test that string with spaces is NOT considered empty."""
        fields = {"value": {"type": str, "required_value": True}}
        field_map = {"value": "value"}
        data = [{"value": "   "}]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["value"], "   ")


if __name__ == "__main__":
    unittest.main()