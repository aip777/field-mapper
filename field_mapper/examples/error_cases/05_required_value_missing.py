"""
Example 5: Required Value Missing (ERROR CASE)

This example demonstrates error handling for:
- Empty strings when value is required
- None values when value is required
- Empty lists when value is required
- Empty dicts when value is required
- Note: 0 and False are NOT considered empty
"""

from field_mapper import FieldMapper

# Field mapping
field_map = {
    "name": "full_name",
    "email": "contact_email",
    "bio": "biography",
    "tags": "user_tags",
    "settings": "user_settings",
    "score": "test_score",
    "is_active": "active_status"
}

# All fields require values
fields = {
    "name": {
        "type": str,
        "required_field": True,
        "required_value": True  # Cannot be empty string
    },
    "email": {
        "type": str,
        "required_field": True,
        "required_value": True  # Cannot be empty string
    },
    "bio": {
        "type": str,
        "required_field": True,
        "required_value": True  # Cannot be empty string
    },
    "tags": {
        "type": list,
        "required_field": True,
        "required_value": True  # Cannot be empty list
    },
    "settings": {
        "type": dict,
        "required_field": True,
        "required_value": True  # Cannot be empty dict
    },
    "score": {
        "type": int,
        "required_field": True,
        "required_value": True  # 0 is OK! Not considered empty
    },
    "is_active": {
        "type": bool,
        "required_field": True,
        "required_value": True  # False is OK! Not considered empty
    }
}

# Data with empty required values
data = [
    {
        "name": "",  # ERROR: Empty string
        "email": "alice@example.com",
        "bio": "Developer",
        "tags": ["python"],
        "settings": {"theme": "dark"},
        "score": 95,
        "is_active": True
    },
    {
        "name": "Bob",
        "email": "bob@example.com",
        "bio": "",  # ERROR: Empty string
        "tags": [],  # ERROR: Empty list
        "settings": {"lang": "en"},
        "score": 0,  # OK! 0 is valid
        "is_active": True
    },
    {
        "name": "Charlie",
        "email": "charlie@example.com",
        "bio": "Engineer",
        "tags": ["java"],
        "settings": {},  # ERROR: Empty dict
        "score": 50,
        "is_active": False  # OK! False is valid
    },
    {
        "name": "Diana",
        "email": "",  # ERROR: Empty string
        "bio": "",  # ERROR: Empty string
        "tags": ["react", "vue"],
        "settings": {"notifications": True},
        "score": 0,
        "is_active": False
    }
]

# Process data
mapper = FieldMapper(fields, field_map)
result = mapper.process(data)

print("=" * 60)
print("ERROR CASE: Required Value Missing")
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
print("  - Empty strings ('') are invalid for required_value")
print("  - Empty lists ([]) are invalid for required_value")
print("  - Empty dicts ({}) are invalid for required_value")
print("  - But 0 and False are VALID (not empty!)")
print("  - First record: empty name")
print("  - Second record: empty bio and tags")
print("  - Third record: empty settings")
print("  - Fourth record: empty email and bio")
print("=" * 60)