"""
Example 2: Invalid Data Types (ERROR CASE)

This example demonstrates error handling for:
- Type mismatches (int vs str, list vs dict, etc.)
- Clear error messages showing expected vs actual types
"""

from field_mapper import FieldMapper

# Field mapping
field_map = {
    "name": "full_name",
    "age": "user_age",
    "email": "contact_email",
    "tags": "user_tags",
    "metadata": "user_metadata"
}

# Field definitions with specific types
fields = {
    "name": {
        "type": str,  # Expects string
        "required_field": True,
        "required_value": True
    },
    "age": {
        "type": int,  # Expects integer
        "required_field": True,
        "required_value": True
    },
    "email": {
        "type": str,  # Expects string
        "required_field": True,
        "required_value": True
    },
    "tags": {
        "type": list,  # Expects list
        "required_field": True,
        "required_value": True
    },
    "metadata": {
        "type": dict,  # Expects dict
        "required_field": True,
        "required_value": True
    }
}

# Data with type mismatches
data = [
    {
        "name": "Alice",
        "age": "30",  # ERROR: String instead of int
        "email": "alice@example.com",
        "tags": ["python", "java"],
        "metadata": {"level": "senior"}
    },
    {
        "name": 12345,  # ERROR: Int instead of string
        "age": 25,
        "email": "bob@example.com",
        "tags": "python,java",  # ERROR: String instead of list
        "metadata": {"level": "junior"}
    },
    {
        "name": "Charlie",
        "age": 30,
        "email": ["charlie@example.com"],  # ERROR: List instead of string
        "tags": ["react"],
        "metadata": ["key", "value"]  # ERROR: List instead of dict
    }
]

# Process data
mapper = FieldMapper(fields, field_map)
result = mapper.process(data)

print("=" * 60)
print("ERROR CASE: Invalid Data Types")
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
print("  - First record: age should be int, not str")
print("  - Second record: name should be str, tags should be list")
print("  - Third record: email should be str, metadata should be dict")
print("  - Error messages show: 'expected <type>, got <type>'")
print("=" * 60)