# Field Mapper

Field Mapper is a Python library that helps you validate and transform data. Perfect for when you need to work with APIs, clean up messy data, or make sure your data is in the right format.

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Table of Contents

- [What does it do?](#what-does-it-do)
- [Installation](#installation)
- [Quick Example](#quick-example)
- [Key Features](#key-features)
- [Core Concepts](#core-concepts)
- [Usage Guide](#usage-guide)
  - [Basic Validation](#1-basic-validation)
  - [Custom Validators](#2-custom-validators)
  - [Working with Nested Data](#3-working-with-nested-data)
  - [Optional Fields](#4-optional-fields)
  - [Lists and Dictionaries](#5-lists-and-dictionaries)
  - [Finding Duplicates](#6-finding-duplicates)
- [Field Definition Reference](#field-definition-reference)
- [Error Handling](#error-handling)
- [Common Use Cases](#common-use-cases)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Why Field Mapper?

Field Mapper solves common data integration challenges:

- **Third-Party APIs**: Transform external API responses to your internal format
- **Data Validation**: Ensure data quality before processing
- **Field Mapping**: Rename fields from source to target naming conventions
- **Nested Structures**: Extract values from deeply nested JSON/dict structures
- **Type Safety**: Validate data types and constraints
- **Error Reporting**: Get detailed, actionable error messages

**Before Field Mapper:**
```python
# Manual validation - tedious and error-prone
for item in data:
    if 'name' not in item or not item['name']:
        raise ValueError("Missing name")
    if not isinstance(item['age'], int):
        raise ValueError("Invalid age type")
    if len(item['email']) > 100:
        raise ValueError("Email too long")
```

**With Field Mapper:**
```python
fields = {
    "name": {"type": str, "required_field": True, "required_value": True},
    "age": {"type": int, "required_field": True},
    "email": {"type": str, "max_length": 100}
}
result = FieldMapper(fields, field_map).process(data)
```

---

## Installation

```bash
pip install field-mapper
```

Requires Python 3.7 or higher.

---

## Quick Example

Here's how simple it is to use:

```python
from field_mapper import FieldMapper

field_map = {
    "name": "full_name",
    "email": "contact_email"
}

fields = {
    "name": {
        "type": str,
        "max_length": 50,
        "required_field": True,
        "required_value": True
    },
    "email": {
        "type": str,
        "max_length": 100,
        "required_field": True,
        "required_value": True
    }
}

data = [
    {"name": "Alice Johnson", "email": "alice@example.com"},
    {"name": "Bob Smith", "email": "bob@example.com"}
]

mapper = FieldMapper(fields, field_map)
result = mapper.process(data)

print(result)
# [{'full_name': 'Alice Johnson', 'contact_email': 'alice@example.com'},
#  {'full_name': 'Bob Smith', 'contact_email': 'bob@example.com'}]
```

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Type Validation** | Validate `str`, `int`, `bool`, `list`, `dict`, `float` |
| **Field Mapping** | Rename fields from source to target format |
| **Nested Extraction** | Extract data from complex nested structures using dot notation and array indexing |
| **Custom Validators** | Add your own validation logic for any field |
| **Length Constraints** | Enforce `max_length` on strings, lists, and dicts |
| **Optional Fields** | Flexible required/optional configurations |
| **Duplicate Detection** | Automatically detect and handle duplicate entries |
| **Rich Error Messages** | Detailed, actionable error reporting |
| **Zero Dependencies** | Pure Python with no external dependencies |

---

## Core Concepts

### The Two Dictionaries

You need two things to use Field Mapper:

**1. field_map** - Tells it how to rename fields
```python
field_map = {
    "old_name": "new_name"
}
```

**2. fields** - Tells it how to validate fields
```python
fields = {
    "old_name": {
        "type": str,
        "max_length": 100,
        "required_field": True,
        "required_value": True,
        "custom": my_function,
        "position": "path"
    }
}
```

### Important: Empty vs Valid Values

Field Mapper knows the difference between "empty" and valid but falsy values:

**These are considered empty:**
- `None`
- `""` (empty string)
- `[]` (empty list)
- `{}` (empty dict)

**These are NOT empty (they're valid!):**
- `0` - Zero is a valid number
- `False` - False is a valid boolean
- `" "` - Spaces are valid

This matters when you set `required_value: True`. A field with value `0` or `False` will pass validation.

---

## Usage Guide

### 1. Basic Validation

Let's validate some user data:

```python
from field_mapper import FieldMapper

field_map = {
    "name": "full_name",
    "age": "user_age",
    "email": "contact_email"
}

fields = {
    "name": {
        "type": str,
        "max_length": 50,
        "required_field": True,
        "required_value": True
    },
    "age": {
        "type": int,
        "required_field": True,
        "required_value": True
    },
    "email": {
        "type": str,
        "max_length": 100,
        "required_field": True,
        "required_value": True
    }
}

data = [
    {"name": "Alice", "age": 30, "email": "alice@example.com"},
    {"name": "Bob", "age": 25, "email": "bob@example.com"}
]

mapper = FieldMapper(fields, field_map)
result = mapper.process(data)

if mapper.error:
    print("Something went wrong:", mapper.error)
else:
    print("Success!", result)
```

### 2. Custom Validators

Want to add your own validation rules? Easy:

```python
def validate_email(value: str) -> bool:
    """Check if email looks valid"""
    return "@" in value and "." in value

def validate_age(value: int) -> bool:
    """Check if age is reasonable"""
    return 0 < value < 150

fields = {
    "email": {
        "type": str,
        "custom": validate_email
    },
    "age": {
        "type": int,
        "custom": validate_age
    }
}
```

You can either return `True`/`False` or raise an exception with a custom error message:

```python
def validate_email(value: str):
    """Raises an error if invalid"""
    if "@" not in value:
        raise ValueError(f"Email must contain @: {value}")
    return True
```

### 3. Working with Nested Data

Got complex JSON structures? No problem:

```python
data = [{
    "email": ["alice@work.com", "alice@personal.com"],
    "phone": {
        "mobile": "+1-555-0001",
        "home": "+1-555-0002"
    },
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "zip": "10001"
    }
}]

field_map = {
    "email[0]": "primary_email",
    "phone.mobile": "mobile_number",
    "address.city": "city"
}

fields = {
    "email": {
        "type": list,
        "position": "email[0]",
        "required_field": True
    },
    "phone": {
        "type": dict,
        "position": "phone.mobile",
        "required_field": True
    },
    "address": {
        "type": dict,
        "position": "address.city",
        "required_field": True
    }
}

mapper = FieldMapper(fields, field_map)
result = mapper.process(data)

print(result[0])
# {'primary_email': 'alice@work.com', 'mobile_number': '+1-555-0001', 'city': 'New York'}
```

**Position syntax you can use:**
- `field[0]` - Get first item from a list
- `field.property` - Get a nested property
- `field[0].property` - Get property from first list item
- `field[].property` - Get property from ALL list items

**Key thing to remember:** The `type` checks the source structure (is it a list or dict?), and `custom` validators check the extracted value.

### 4. Optional Fields

Sometimes fields are optional. You have two controls:

```python
fields = {
    "name": {
        "type": str,
        "required_field": True,
        "required_value": True
    },
    "phone": {
        "type": str,
        "required_field": False,
        "required_value": False
    },
    "age": {
        "type": int,
        "required_field": True,
        "required_value": False
    }
}

data = [
    {"name": "Alice", "phone": "555-1234", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "phone": "", "age": 0},
]
```

**Quick guide:**

| What you want | required_field | required_value |
|---------------|----------------|----------------|
| Field must exist and have a value | `True` | `True` |
| Field must exist but can be empty | `True` | `False` |
| Field is optional but must have value if present | `False` | `True` |
| Field is completely optional | `False` | `False` |

### 5. Lists and Dictionaries

You can validate lists and dicts too:

```python
fields = {
    "tags": {
        "type": list,
        "max_length": 10,
        "required_value": True
    },
    "metadata": {
        "type": dict,
        "max_length": 5,
        "required_value": False
    }
}

data = [
    {
        "tags": ["python", "javascript", "docker"],
        "metadata": {"level": "senior"}
    },
    {
        "tags": ["java"],
        "metadata": {}
    }
]
```

### 6. Finding Duplicates

Need to catch duplicate entries?

```python
data = [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"},
    {"name": "Alice", "email": "alice@example.com"},
]

mapper = FieldMapper(fields, field_map)
result = mapper.process(data, skip_duplicate=True)

if mapper.error:
    print("Found duplicates!")
```

---

## Field Definition Reference

Here's everything you can put in a field definition:

```python
fields = {
    "field_name": {
        "type": str,
        "max_length": 100,
        "required_field": True,
        "required_value": True,
        "custom": validator_func,
        "position": "path"
    }
}
```

**Available types:** `str`, `int`, `float`, `bool`, `list`, `dict`

---

## Error Handling

Always check for errors after processing:

```python
mapper = FieldMapper(fields, field_map)
result = mapper.process(data)

if mapper.error:
    print("Validation failed:")
    for error in mapper.error:
        print(f"  - {error}")
    # result will be an empty list []
else:
    print(f"Success! Processed {len(result)} records")
    # Do something with result
    for record in result:
        save_to_database(record)
```

**Common error messages you might see:**

```
Missing required field: 'email'
Invalid type for field 'age': expected int, got str
Field 'name' (str) exceeds max length of 50 (current: 75)
Required value missing or empty for field: 'email'
Custom validation failed for field: 'email'
Duplicate data detected
```

---

## Common Use Cases

### Use Case 1: Working with External APIs

```python
# API returns this format
api_response = {
    "firstName": "Alice",
    "lastName": "Johnson",
    "emailAddress": "alice@example.com"
}

# Convert to your format
field_map = {
    "firstName": "first_name",
    "lastName": "last_name",
    "emailAddress": "email"
}

fields = {
    "firstName": {"type": str, "max_length": 50},
    "lastName": {"type": str, "max_length": 50},
    "emailAddress": {"type": str, "max_length": 100}
}

mapper = FieldMapper(fields, field_map)
result = mapper.process([api_response])
# {'first_name': 'Alice', 'last_name': 'Johnson', 'email': 'alice@example.com'}
```

### Use Case 2: Validating Form Data

```python
def validate_password(value: str) -> bool:
    """Password needs 8+ chars with uppercase, lowercase, and number"""
    if len(value) < 8:
        return False
    has_upper = any(c.isupper() for c in value)
    has_lower = any(c.islower() for c in value)
    has_digit = any(c.isdigit() for c in value)
    return has_upper and has_lower and has_digit

fields = {
    "username": {
        "type": str,
        "max_length": 20,
        "required_value": True
    },
    "email": {
        "type": str,
        "max_length": 100,
        "required_value": True,
        "custom": validate_email
    },
    "password": {
        "type": str,
        "max_length": 100,
        "required_value": True,
        "custom": validate_password
    }
}
```

### Use Case 3: Cleaning Up Data

```python
# Before: messy data with inconsistent fields
messy_data = [
    {"usr_nm": "Alice", "emp_id": 123},
    {"usr_nm": "Bob", "emp_id": 456}
]

# After: clean, standardized data
field_map = {
    "usr_nm": "user_name",
    "emp_id": "employee_id"
}

mapper = FieldMapper(fields, field_map)
clean_data = mapper.process(messy_data)
# [{'user_name': 'Alice', 'employee_id': 123}, ...]
```

---

## Troubleshooting

### "Missing required field" but the field exists

**Problem:** Field names are case-sensitive

```python
# Won't work - case mismatch
data = {"Name": "Alice"}
fields = {"name": {...}}

# Fix - match exactly
data = {"name": "Alice"}
fields = {"name": {...}}
```

### "Invalid type" for nested data

**Problem:** You're checking the wrong type

```python
# Wrong - source is a list, not a string
data = {"emails": ["alice@example.com"]}
fields = {
    "emails": {
        "type": str,
        "position": "emails[0]"
    }
}

# Right - check the source type
fields = {
    "emails": {
        "type": list,
        "position": "emails[0]"
    }
}
```

### Custom validator not working

**Problem:** Don't call the function, just pass it

```python
# Wrong - calling the function
fields = {
    "email": {
        "custom": validate_email() 
    }
}

# Right - pass the function
fields = {
    "email": {
        "custom": validate_email 
    }
}
```

---

## Contributing

Want to help make Field Mapper better? Great!

- **Found a bug?** [Open an issue](https://github.com/aip777/field-mapper/issues)
- **Have an idea?** Tell us about it in an issue
- **Want to contribute code?** Fork the repo and submit a pull request

### Contributors:
- [Ariful Islam Palash](https://github.com/aip777) - Creator
- [Md Lutfor Rahman](https://github.com/shifat151) - Core Contributor

---

**Links:**
- [PyPI Package](https://pypi.org/project/field-mapper/)
- [GitHub Repository](https://github.com/aip777/field-mapper)
- [Report Issues](https://github.com/aip777/field-mapper/issues)