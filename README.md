### Field Mapper: Documentation

Field Mapper is a Python library for validating, mapping, and transforming data fields. It supports type checking, length constraints, optional fields, and custom validation rules, making it perfect for structured data validation.

### Installation
Install the library using pip
```bat
pip install field-mapper
```

### Quick Start
1. Define Fields
Create a dictionary to define the rules for your data fields.
```bat
fields = {
    "name": {"type": str, "max_length": 50},
    "email": {"type": str, "max_length": 100, "custom": validate_email},
    "phone": {"type": str, "max_length": 15, "required": False},
}
```

2. Prepare Data
The input should be a list of dictionaries.
```bat
data = [
    {"name": "Alice", "email": "alice@example.com", "phone": "123456789"},
    {"name": "Bob", "email": "invalid-email", "phone": "987654321"},
]
```

3. Create a Field Mapper Instance
Initialize the FieldMapper class.
```bat
from field_mapper.mapper import FieldMapper
mapper = FieldMapper(fields)
```

4. Data Process
Use the process method to check and transform the data.
```bat
try:  
    processed_data = mapper.process(data)  
    print(processed_data)  
except Exception as exc:  
    print(exc)  

#Output: 
[
    {"name": "Alice", "email": "alice@example.com", "phone": "123456789"}
]

```

Custom Validation
Define custom validation logic for specific fields.

```bat
def validate_email(value):  
    import re  
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):  
        raise ValueError(f"Invalid email address: {value}")  

#Add the custom validator in the field definition:
fields = {
    "email": {"type": str, "custom": validate_email},
}

```

Optional Fields
Mark fields as optional with required: False. 
If check_optional_fields=True is set, their presence is mandatory but values can be empty:
```bat
fields = {
    "phone": {"type": str, "max_length": 15, "required": False},
}
mapper = FieldMapper(fields, check_optional_fields=True)  

```

### Example usage
```bat
from field_mapper.mapper import FieldMapper

def validate_email(value: str) -> bool:
    return "@" in value and "." in value

fields = {
    "name": {"type": str, "max_length": 50, "required": True},
    "email": {"type": str, "max_length": 100, "required": True, "custom": validate_email},
    "phone": {"type": str, "max_length": 15, "required": False}
}
field_map = {
    "name": "full_name",
    "email": "contact_email",
    "phone": "mobile_number"
}

mapper = FieldMapper(fields, field_map)

data = [
    {"name": "Alice", "email": "alice@example.com", "phone": "1234567890"},
    {"name": "Bob", "email": "invalid-email"},
    {"name": "Charlie", "email": "charlie@example.com"}
]
processed_data = mapper.process(data)
print(processed_data)

```
