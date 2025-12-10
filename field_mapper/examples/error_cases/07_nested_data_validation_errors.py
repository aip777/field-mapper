"""
Example 7: Nested Data Validation Errors (ERROR CASE)

This example demonstrates error handling for:
- Missing nested fields
- Wrong types in nested structures
- Custom validation on extracted nested values
"""

from field_mapper import FieldMapper


def validate_email(value: str) -> bool:
    """Validate extracted email"""
    return "@" in value and "." in value


field_map = {
    "name": "full_name",
    "email[0]": "primary_email",
    "phone.mobile": "mobile_number",
    "address.city": "city",
    "salary[0].amount": "current_salary"
}

fields = {
    "name": {
        "type": str,
        "position": "name",
        "required_field": True,
        "required_value": True
    },
    "email": {
        "type": list,
        "position": "email[0]",
        "required_field": True,
        "required_value": True,
        "custom": validate_email
    },
    "phone": {
        "type": dict,
        "position": "phone.mobile",
        "required_field": True,
        "required_value": True
    },
    "address": {
        "type": dict,
        "position": "address.city",
        "required_field": True,
        "required_value": True
    },
    "salary": {
        "type": list,
        "position": "salary[0].amount",
        "required_field": True,
        "required_value": True
    }
}

data = [
    {
        "name": "Alice",
        "email": "alice@example.com",
        "phone": {"mobile": "555-0001"},
        "address": {"city": "New York"},
        "salary": [{"amount": 95000}]
    },
    {
        "name": "Bob",
        "email": ["invalid-email"],
        "phone": "+1-555-1001",
        "address": {"city": "San Francisco"},
        "salary": [{"amount": 110000}]
    },
    {
        "name": "Charlie",
        "email": ["charlie@example.com"],
        "phone": {"mobile": "555-2001"},
        "salary": [{"amount": 85000}]
    },
    {
        "name": "Diana",
        "email": ["diana@example.com"],
        "phone": {"home": "555-3001"},
        "address": {"street": "123 Main"},
        "salary": "75000"
    }
]

mapper = FieldMapper(fields, field_map)
result = mapper.process(data)

print("=" * 60)
print("ERROR CASE: Nested Data Validation Errors")
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
print("  - First record: email should be list, not string")
print("  - Second record: email fails custom validation, phone should be dict")
print("  - Third record: missing address field")
print("  - Fourth record: salary should be list, not string")
print("  - Type validation checks SOURCE data structure")
print("  - Custom validation checks EXTRACTED value")
print("=" * 60)