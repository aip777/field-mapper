"""
Example 1: Basic Field Validation and Mapping (SUCCESS)

This example demonstrates:
- Basic type validation (str, int)
- Required and optional fields
- Field mapping (renaming fields)
- Max length validation
"""

from field_mapper import FieldMapper

field_map = {
    "name": "full_name",
    "email": "contact_email",
    "phone": "mobile_number",
    "age": "user_age"
}

fields = {
    "name": {
        "type": str,
        "max_length": 50,
        "required_field": True,
        "required_value": True
    },
    "email": {
        "type": str,
        "max_length": 100,
        "required_field": True,
        "required_value": True
    },
    "phone": {
        "type": str,
        "max_length": 15,
        "required_field": False,
        "required_value": False
    },
    "age": {
        "type": int,
        "required_field": True,
        "required_value": True
    }
}

data = [
    {"name": "Alice Johnson", "email": "alice@example.com", "phone": "1234567890", "age": 30},
    {"name": "Bob Smith", "email": "bob@example.com", "age": 25},
    {"name": "Charlie Brown", "email": "charlie@example.com", "phone": "9876543210", "age": 0}
]

mapper = FieldMapper(fields, field_map)
result = mapper.process(data)

print("=" * 60)
print("SUCCESS: Basic Validation and Mapping")
print("=" * 60)
print(f"\nProcessed {len(result)} records successfully!")
print("\nResults:")
for idx, record in enumerate(result, 1):
    print(f"\n  Record {idx}:")
    for key, value in record.items():
        print(f"    {key}: {value}")

print(f"\nErrors: {mapper.error if mapper.error else 'None'}")
print("=" * 60)