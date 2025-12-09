"""
Example 5: Complex Data Types (SUCCESS)

This example demonstrates:
- Validating list types
- Validating dict types
- Max length on lists and dicts
- Handling complex nested structures
"""

from field_mapper import FieldMapper

# Field mapping
field_map = {
    "name": "full_name",
    "tags": "user_tags",
    "metadata": "user_metadata",
    "emails": "email_list",
    "contacts": "contact_info"
}

# Field validation for complex types
fields = {
    "name": {
        "type": str,
        "max_length": 50,
        "required_field": True,
        "required_value": True
    },
    "tags": {
        "type": list,
        "max_length": 10,         # Max 10 tags allowed
        "required_field": True,
        "required_value": True
    },
    "metadata": {
        "type": dict,
        "max_length": 5,          # Max 5 keys in dict
        "required_field": True,
        "required_value": False   # Can be empty dict
    },
    "emails": {
        "type": list,
        "max_length": 5,          # Max 5 emails
        "required_field": True,
        "required_value": True
    },
    "contacts": {
        "type": dict,
        "required_field": False,  # Optional
        "required_value": False
    }
}

# Data with complex types
data = [
    {
        "name": "Alice Johnson",
        "tags": ["python", "javascript", "docker"],
        "metadata": {
            "department": "Engineering",
            "level": "Senior",
            "location": "NYC"
        },
        "emails": ["alice@work.com", "alice@personal.com"],
        "contacts": {
            "slack": "@alice",
            "github": "alice-dev"
        }
    },
    {
        "name": "Bob Smith",
        "tags": ["java", "kubernetes"],
        "metadata": {},           # Empty dict is valid
        "emails": ["bob@company.org"],
        "contacts": {
            "linkedin": "bob-smith"
        }
    },
    {
        "name": "Charlie Brown",
        "tags": ["react", "nodejs", "aws", "terraform"],
        "metadata": {
            "department": "DevOps",
            "level": "Lead"
        },
        "emails": ["charlie@example.com"]
        # contacts is optional, can be missing
    }
]

# Process data
mapper = FieldMapper(fields, field_map)
result = mapper.process(data)

print("=" * 60)
print("SUCCESS: Complex Data Types")
print("=" * 60)
print(f"\nProcessed {len(result)} records with complex types!")
print("\nDemonstrating:")
print("  - List type validation with max_length")
print("  - Dict type validation with max_length")
print("  - Empty collections as valid values")
print("\nResults:")
for idx, record in enumerate(result, 1):
    print(f"\n  Record {idx}:")
    for key, value in record.items():
        if isinstance(value, (list, dict)):
            print(f"    {key} ({type(value).__name__}, len={len(value)}): {value}")
        else:
            print(f"    {key}: {value}")

print(f"\nErrors: {mapper.error if mapper.error else 'None'}")
print("=" * 60)