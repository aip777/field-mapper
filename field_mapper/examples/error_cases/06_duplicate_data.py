"""
Example 6: Duplicate Data Detection (ERROR CASE)

This example demonstrates error handling for:
- Detecting duplicate entries when skip_duplicate=True
- DuplicateDataError exception
- Showing which records are duplicates
"""

from field_mapper import FieldMapper

field_map = {
    "name": "full_name",
    "email": "contact_email",
    "department": "dept"
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
    "department": {
        "type": str,
        "required_field": True,
        "required_value": True
    }
}

data = [
    {"name": "Alice", "email": "alice@example.com", "department": "Engineering"},
    {"name": "Bob", "email": "bob@example.com", "department": "Sales"},
    {"name": "Alice", "email": "alice@example.com", "department": "Engineering"},
    {"name": "Charlie", "email": "charlie@example.com", "department": "Marketing"},
    {"name": "Bob", "email": "bob@example.com", "department": "Sales"},
    {"name": "Bob", "email": "bob@example.com", "department": "Sales"},
]

mapper = FieldMapper(fields, field_map)
result = mapper.process(data, skip_duplicate=True)

print("=" * 60)
print("ERROR CASE: Duplicate Data Detection")
print("=" * 60)
print(f"\nTotal records in input: {len(data)}")
print(f"Processed: {len(result)} records")
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
print("  - When skip_duplicate=True, duplicates are detected")
print("  - DuplicateDataError is raised")
print("  - Duplicate records are shown in error.problematic_data")
print("  - Processing stops at first duplicate set")
print("  - Returns empty list []")
print("\nDuplicates in this data:")
print("  - Record 3 is duplicate of record 1 (Alice)")
print("  - Records 5 and 6 are duplicates of record 2 (Bob)")
print("=" * 60)