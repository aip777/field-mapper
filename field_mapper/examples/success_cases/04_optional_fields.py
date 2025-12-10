"""
Example 4: Optional Fields and Values (SUCCESS)

This example demonstrates:
- required_field: False (field can be absent)
- required_value: False (field can be empty/None/0/False)
- Handling of falsy values (0, False, empty string)
- Mix of required and optional fields
"""

from field_mapper import FieldMapper

field_map = {
    "name": "full_name",
    "email": "contact_email",
    "phone": "phone_number",
    "age": "user_age",
    "score": "test_score",
    "is_active": "active_status",
    "notes": "additional_notes"
}

fields = {
    "name": {
        "type": str,
        "required_field": True,
        "required_value": True
    },
    "email": {
        "type": str,
        "required_field": True,
        "required_value": True
    },
    "phone": {
        "type": str,
        "required_field": False,
        "required_value": False
    },
    "age": {
        "type": int,
        "required_field": True,
        "required_value": False
    },
    "score": {
        "type": int,
        "required_field": False,
        "required_value": False
    },
    "is_active": {
        "type": bool,
        "required_field": True,
        "required_value": False
    },
    "notes": {
        "type": str,
        "required_field": False,
        "required_value": False
    }
}

data = [
    {
        "name": "Alice",
        "email": "alice@example.com",
        "phone": "1234567890",
        "age": 30,
        "score": 95,
        "is_active": True,
        "notes": "Great employee"
    },
    {
        "name": "Bob",
        "email": "bob@example.com",
        "age": 0,
        "score": 0,
        "is_active": False,
        "notes": ""
    },
    {
        "name": "Charlie",
        "email": "charlie@example.com",
        "phone": "",
        "age": 25,
        "is_active": True
    },
    {
        "name": "Diana",
        "email": "diana@example.com",
        "age": 28,
        "is_active": False,
    }
]

mapper = FieldMapper(fields, field_map)
result = mapper.process(data)

print("=" * 60)
print("SUCCESS: Optional Fields and Values")
print("=" * 60)
print(f"\nProcessed {len(result)} records with optional fields!")
print("\nDemonstrating:")
print("  - Optional fields can be absent")
print("  - Optional values can be 0, False, or empty string")
print("  - Required fields must be present")
print("\nResults:")
for idx, record in enumerate(result, 1):
    print(f"\n  Record {idx}:")
    for key, value in record.items():
        value_display = repr(value) if value == "" or value is None else value
        print(f"    {key}: {value_display}")

print(f"\nErrors: {mapper.error if mapper.error else 'None'}")
print("=" * 60)