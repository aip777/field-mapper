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


# Field mapping with nested paths
field_map = {
    "name": "full_name",
    "email[0]": "primary_email",
    "phone.mobile": "mobile_number",
    "address.city": "city",
    "salary[0].amount": "current_salary"
}

# Field validation - validates SOURCE structure
fields = {
    "name": {
        "type": str,
        "position": "name",
        "required_field": True,
        "required_value": True
    },
    "email": {
        "type": list,  # Source must be a list
        "position": "email[0]",
        "required_field": True,
        "required_value": True,
        "custom": validate_email  # Validates extracted value
    },
    "phone": {
        "type": dict,  # Source must be a dict
        "position": "phone.mobile",
        "required_field": True,
        "required_value": True
    },
    "address": {
        "type": dict,  # Source must be a dict
        "position": "address.city",
        "required_field": True,
        "required_value": True
    },
    "salary": {
        "type": list,  # Source must be a list
        "position": "salary[0].amount",
        "required_field": True,
        "required_value": True
    }
}

# Data with nested validation errors
data = [
    {
        "name": "Alice",
        "email": "alice@example.com",  # ERROR: Should be list, not string
        "phone": {"mobile": "555-0001"},
        "address": {"city": "New York"},
        "salary": [{"amount": 95000}]
    },
    {
        "name": "Bob",
        "email": ["invalid-email"],  # ERROR: Custom validation fails (no @ or .)
        "phone": "+1-555-1001",  # ERROR: Should be dict, not string
        "address": {"city": "San Francisco"},
        "salary": [{"amount": 110000}]
    },
    {
        "name": "Charlie",
        "email": ["charlie@example.com"],
        "phone": {"mobile": "555-2001"},
        # ERROR: Missing address (required field)
        "salary": [{"amount": 85000}]
    },
    {
        "name": "Diana",
        "email": ["diana@example.com"],
        "phone": {"home": "555-3001"},  # Has phone dict, but no 'mobile' key
        "address": {"street": "123 Main"},  # Has address dict, but no 'city' key
        "salary": "75000"  # ERROR: Should be list, not string
    }
]

# Process data
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