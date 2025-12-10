"""
Example 3: Max Length Validation Errors (ERROR CASE)

This example demonstrates error handling for:
- String exceeding max_length
- List exceeding max_length
- Dict exceeding max_length (number of keys)
- Detailed error messages showing current vs max length
"""

from field_mapper import FieldMapper

field_map = {
    "username": "user_name",
    "bio": "biography",
    "tags": "user_tags",
    "settings": "user_settings"
}

fields = {
    "username": {
        "type": str,
        "max_length": 20,
        "required_field": True,
        "required_value": True
    },
    "bio": {
        "type": str,
        "max_length": 100,
        "required_field": True,
        "required_value": True
    },
    "tags": {
        "type": list,
        "max_length": 5,
        "required_field": True,
        "required_value": True
    },
    "settings": {
        "type": dict,
        "max_length": 3,
        "required_field": True,
        "required_value": True
    }
}

data = [
    {
        "username": "this_is_a_very_long_username_that_exceeds_limit",
        "bio": "Software engineer with 10 years of experience",
        "tags": ["python", "java"],
        "settings": {"theme": "dark"}
    },
    {
        "username": "alice",
        "bio": "A" * 150,
        "tags": ["python", "javascript", "docker", "kubernetes", "aws", "react"],
        "settings": {"theme": "dark", "lang": "en"}
    },
    {
        "username": "bob",
        "bio": "DevOps engineer",
        "tags": ["docker"],
        "settings": {
            "theme": "light",
            "lang": "fr",
            "timezone": "UTC",
            "notifications": True
        }
    }
]

mapper = FieldMapper(fields, field_map)
result = mapper.process(data)

print("=" * 60)
print("ERROR CASE: Max Length Exceeded")
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
print("  - First record: username too long (51 > 20)")
print("  - Second record: bio too long (150 > 100), too many tags (6 > 5)")
print("  - Third record: too many settings (4 > 3)")
print("  - Error messages show type, max, and current length")
print("=" * 60)