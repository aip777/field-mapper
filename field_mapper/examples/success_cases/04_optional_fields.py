"""
Example 4: Optional Fields and Values (SUCCESS)

This example demonstrates:
- required_field: False (field can be absent)
- required_value: False (field can be empty/None/0/False)
- Handling of falsy values (0, False, empty string)
- Mix of required and optional fields
"""

from field_mapper import FieldMapper

# Field mapping
field_map = {
    "name": "full_name",
    "email": "contact_email",
    "phone": "phone_number",
    "age": "user_age",
    "score": "test_score",
    "is_active": "active_status",
    "notes": "additional_notes"
}

# Field validation with various optional configurations
fields = {
    "name": {
        "type": str,
        "required_field": True,   # Field must be present
        "required_value": True    # Field must have a non-empty value
    },
    "email": {
        "type": str,
        "required_field": True,   # Field must be present
        "required_value": True    # Field must have a non-empty value
    },
    "phone": {
        "type": str,
        "required_field": False,  # Field can be absent
        "required_value": False   # If present, can be empty
    },
    "age": {
        "type": int,
        "required_field": True,   # Field must be present
        "required_value": False   # Can be 0 (falsy but valid)
    },
    "score": {
        "type": int,
        "required_field": False,  # Field can be absent
        "required_value": False   # Can be 0
    },
    "is_active": {
        "type": bool,
        "required_field": True,   # Field must be present
        "required_value": False   # Can be False (falsy but valid)
    },
    "notes": {
        "type": str,
        "required_field": False,  # Field can be absent
        "required_value": False   # Can be empty string
    }
}

# Data with various optional/falsy values
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
        # phone is missing (optional field)
        "age": 0,              # 0 is valid (newborn baby!)
        "score": 0,            # 0 score is valid
        "is_active": False,    # False is valid
        "notes": ""            # Empty string is valid
    },
    {
        "name": "Charlie",
        "email": "charlie@example.com",
        "phone": "",           # Empty string is valid for optional value
        "age": 25,
        # score is missing (optional field)
        "is_active": True
        # notes is missing (optional field)
    },
    {
        "name": "Diana",
        "email": "diana@example.com",
        "age": 28,
        "is_active": False,
        # Multiple optional fields missing
    }
]

# Process data
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