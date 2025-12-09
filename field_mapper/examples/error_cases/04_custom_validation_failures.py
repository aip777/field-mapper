"""
Example 4: Custom Validation Failures (ERROR CASE)

This example demonstrates error handling for:
- Custom validation functions returning False
- Custom validation functions raising exceptions
- Detailed error messages from custom validators
"""

from field_mapper import FieldMapper
import re


def validate_email(value: str) -> bool:
    """Strict email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    is_valid = bool(re.match(pattern, value))
    if not is_valid:
        # This won't show in error, but False will trigger "Custom validation failed"
        pass
    return is_valid


def validate_phone(value: str):
    """Raise exception for invalid phone"""
    if not value:
        return True
    clean = re.sub(r'[\s\-\(\)]', '', value)
    if not (clean.isdigit() and 10 <= len(clean) <= 15):
        raise ValueError(f"Phone must be 10-15 digits, got: {value}")
    return True


def validate_age(value: int) -> bool:
    """Age range validation"""
    return 0 < value < 150


def validate_username(value: str):
    """Username validation with exception"""
    if len(value) < 3:
        raise ValueError("Username must be at least 3 characters")
    if not value[0].isalpha():
        raise ValueError("Username must start with a letter")
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValueError("Username can only contain letters, numbers, and underscores")
    return True


# Field mapping
field_map = {
    "username": "user_name",
    "email": "contact_email",
    "phone": "phone_number",
    "age": "user_age"
}

# Fields with custom validators
fields = {
    "username": {
        "type": str,
        "required_field": True,
        "required_value": True,
        "custom": validate_username
    },
    "email": {
        "type": str,
        "required_field": True,
        "required_value": True,
        "custom": validate_email
    },
    "phone": {
        "type": str,
        "required_field": False,
        "required_value": False,
        "custom": validate_phone
    },
    "age": {
        "type": int,
        "required_field": True,
        "required_value": True,
        "custom": validate_age
    }
}

# Data with custom validation failures
data = [
    {
        "username": "ab",  # ERROR: Too short (< 3 chars)
        "email": "alice@example.com",
        "phone": "1234567890",
        "age": 30
    },
    {
        "username": "1bob",  # ERROR: Starts with number
        "email": "invalid-email",  # ERROR: Missing @ and domain
        "phone": "123",  # ERROR: Too few digits
        "age": 25
    },
    {
        "username": "charlie@user",  # ERROR: Contains @
        "email": "charlie@example.com",
        "phone": "(555) 123-4567",
        "age": 200  # ERROR: Age > 150
    },
    {
        "username": "diana",
        "email": "diana@test",  # ERROR: Invalid domain
        "age": -5  # ERROR: Age < 0
    }
]

# Process data
mapper = FieldMapper(fields, field_map)
result = mapper.process(data)

print("=" * 60)
print("ERROR CASE: Custom Validation Failures")
print("=" * 60)
print(f"\nProcessed: {len(result)} records")
print(f"Errors found: {len(mapper.error)}")

if mapper.error:
    print("\nDetailed Errors:")
    for idx, error in enumerate(mapper.error, 1):
        print(f"\n--- Error {idx} ---")
        print(error)
else:
    print("\nResults:", result)

print("\n" + "=" * 60)
print("Expected behavior:")
print("  - Username validations catch: too short, starts with number, invalid chars")
print("  - Email validation catches: invalid format")
print("  - Phone validation catches: too few digits")
print("  - Age validation catches: < 0 or > 150")
print("  - Exception messages included in error output")
print("=" * 60)