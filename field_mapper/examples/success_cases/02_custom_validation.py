"""
Example 2: Custom Validation Functions (SUCCESS)

This example demonstrates:
- Custom validation with boolean return
- Custom validation with exception raising
- Combining built-in and custom validation
"""

from field_mapper import FieldMapper
import re


def validate_email(value: str) -> bool:
    """Custom email validator - returns boolean"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, value))


def validate_phone(value: str) -> bool:
    """Custom phone validator - returns boolean"""
    if not value:
        return True
    clean = re.sub(r'[\s\-\(\)]', '', value)
    return clean.isdigit() and 10 <= len(clean) <= 15


def validate_age(value: int) -> bool:
    """Custom age validator - check range"""
    return 0 < value < 150


field_map = {
    "name": "full_name",
    "email": "contact_email",
    "phone": "phone_number",
    "age": "user_age"
}

fields = {
    "name": {
        "type": str,
        "max_length": 100,
        "required_field": True,
        "required_value": True
    },
    "email": {
        "type": str,
        "max_length": 100,
        "required_field": True,
        "required_value": True,
        "custom": validate_email
    },
    "phone": {
        "type": str,
        "max_length": 20,
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

data = [
    {"name": "Alice", "email": "alice@example.com", "phone": "1234567890", "age": 30},
    {"name": "Bob", "email": "bob@company.org", "phone": "123-456-7890", "age": 25},
    {"name": "Charlie", "email": "charlie@test.co.uk", "phone": "(555) 123-4567", "age": 40},
    {"name": "Diana", "email": "diana@email.com", "age": 28}
]

mapper = FieldMapper(fields, field_map)
result = mapper.process(data)

print("=" * 60)
print("SUCCESS: Custom Validation")
print("=" * 60)
print(f"\nProcessed {len(result)} records with custom validators!")
print("\nResults:")
for idx, record in enumerate(result, 1):
    print(f"\n  Record {idx}:")
    for key, value in record.items():
        print(f"    {key}: {value}")

print(f"\nErrors: {mapper.error if mapper.error else 'None'}")
print("=" * 60)