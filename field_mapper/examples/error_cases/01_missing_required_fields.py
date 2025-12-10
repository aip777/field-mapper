from field_mapper import FieldMapper

field_map = {
    "name": "full_name",
    "email": "contact_email",
    "phone": "phone_number",
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
    "phone": {
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
    {"name": "Alice", "email": "alice@example.com", "phone": "1234567890"},
    {"name": "Bob", "email": "bob@example.com"},
    {"email": "charlie@example.com", "phone": "5555555555", "department": "IT"}
]

mapper = FieldMapper(fields, field_map)
result = mapper.process(data)

print("=" * 60)
print("ERROR CASE: Missing Required Fields")
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
print("  - First record: Missing 'department'")
print("  - Second record: Missing 'phone' and 'department'")
print("  - Third record: Missing 'name'")
print("  - All records fail validation")
print("  - Returns empty list []")
print("  - Errors logged in mapper.error")
print("=" * 60)