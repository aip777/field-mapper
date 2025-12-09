"""
Example 3: Nested Data Extraction with Position Parameter (SUCCESS)

This example demonstrates:
- Extracting values from nested dictionaries (dot notation)
- Extracting values from arrays with index (bracket notation)
- Extracting values from nested arrays in dictionaries
- Dynamic array extraction with []
- Validating source structure while extracting nested values
"""

from field_mapper import FieldMapper


def validate_email(value: str) -> bool:
    """Validate extracted email"""
    return "@" in value and "." in value


# Field mapping with nested paths
field_map = {
    "name": "full_name",
    "email[0]": "primary_email",              # Extract first email from array
    "phone.mobile": "mobile_number",          # Extract from nested dict
    "address.city": "city",                   # Extract nested property
    "salary[0].amount": "current_salary",     # Extract from nested array of dicts
    "skills[].name": "skill_names"            # Extract field from all array items
}

# Field validation rules
# Note: 'type' validates the SOURCE data structure, not extracted value
fields = {
    "name": {
        "type": str,
        "position": "name",
        "max_length": 100,
        "required_field": True,
        "required_value": True
    },
    "email": {
        "type": list,                          # Source is a list
        "position": "email[0]",                # Extract first item
        "max_length": 3,                       # Max 3 emails in source
        "required_field": True,
        "required_value": True,
        "custom": validate_email               # Validate extracted value
    },
    "phone": {
        "type": dict,                          # Source is a dict
        "position": "phone.mobile",            # Extract mobile field
        "required_field": True,
        "required_value": True
    },
    "address": {
        "type": dict,                          # Source is a dict
        "position": "address.city",            # Extract city field
        "required_field": True,
        "required_value": True
    },
    "salary": {
        "type": list,                          # Source is a list
        "position": "salary[0].amount",        # Extract amount from first salary
        "required_field": True,
        "required_value": True
    },
    "skills": {
        "type": list,                          # Source is a list
        "position": "skills[].name",           # Extract name from all items
        "required_field": True,
        "required_value": True
    }
}

# Complex nested data
data = [
    {
        "name": "Alice Johnson",
        "email": ["alice@work.com", "alice@personal.com"],
        "phone": {
            "mobile": "+1-555-0001",
            "home": "+1-555-0002"
        },
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "zip": "10001"
        },
        "salary": [
            {"year": 2024, "amount": 95000},
            {"year": 2023, "amount": 85000}
        ],
        "skills": [
            {"name": "Python", "level": "Expert"},
            {"name": "JavaScript", "level": "Intermediate"},
            {"name": "SQL", "level": "Advanced"}
        ]
    },
    {
        "name": "Bob Smith",
        "email": ["bob@company.org"],
        "phone": {
            "mobile": "+1-555-1001",
            "work": "+1-555-1002"
        },
        "address": {
            "street": "456 Oak Ave",
            "city": "San Francisco",
            "zip": "94102"
        },
        "salary": [
            {"year": 2024, "amount": 110000}
        ],
        "skills": [
            {"name": "Java", "level": "Expert"},
            {"name": "Docker", "level": "Advanced"}
        ]
    }
]

# Process data
mapper = FieldMapper(fields, field_map)
result = mapper.process(data)

print("=" * 60)
print("SUCCESS: Nested Data Extraction")
print("=" * 60)
print(f"\nProcessed {len(result)} records with nested data extraction!")
print("\nResults:")
for idx, record in enumerate(result, 1):
    print(f"\n  Record {idx}:")
    for key, value in record.items():
        if isinstance(value, list):
            print(f"    {key}: {value}")
        else:
            print(f"    {key}: {value}")

print(f"\nErrors: {mapper.error if mapper.error else 'None'}")
print("=" * 60)