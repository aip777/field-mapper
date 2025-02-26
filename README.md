### Field Mapper: Documentation
Field Mapper is a Python library designed for validating, mapping, and transforming data fields. It is particularly useful for integrating third-party systems, ensuring compatibility when third-party fields and internal system fields differ. The library supports type checking, length constraints, optional fields, custom validation rules, and seamless data transformation for structured data validation.
### Installation
Install the library using pip
```bash
pip install field-mapper
```

### Quick Start
1. Define Fields
Create a field map dictionary.
Also, Create a fields dictionary to define the rules for your data fields.
```python
field_map = {
    "name": "full_name",
    "email": "contact_email",
    "phone": "mobile_number",
    "income": "monthly_income"
}
fields = {
    "name": {"type": str, "max_length": 50, "required_field": True, "required_value":True},
    "email": {"type": str, "max_length": 100, "required_field": True, "required_value":True},
    "phone": {"type": str, "max_length": 15, "required_field": False, "required_value":False},
    "income": {"type": int, "max_length": 15, "required_field": True, "required_value":False}
}
```

2. Prepare Data
The input should be a list of dictionaries.
```python
data = [
    {"name": "Alice", "email": "alice@example.com", "phone": "1234567890"},
    {"name": "Bob", "email": "charlieexample.com", "phone": "453543535", "income":0},
    {"name": "Charlie", "email": "charlie@example.com", "phone": "34534523", "income":0}
]
```

3. Data Process
Use the process method to check and transform the data.

```python
from field_mapper import FieldMapper

field_map = {
    "name": "full_name",
    "email": "contact_email",
    "phone": "mobile_number",
    "income": "monthly_income"
}

fields = {
    "name": {"type": str, "max_length": 50, "required_field": True, "required_value":True},
    "email": {"type": str, "max_length": 100, "required_field": True, "required_value":True},
    "phone": {"type": str, "max_length": 15, "required_field": False, "required_value":False},
    "income": {"type": int, "max_length": 15, "required_field": True, "required_value":False}
}

data = [
    {"name": "Alice", "email": "alice@example.com", "phone": "1234567890"},
    {"name": "Bob", "email": "charlieexample.com", "phone": "453543535", "income":0},
    {"name": "Charlie", "email": "charlie@example.com", "phone": "34534523", "income":0}
]

mapper = FieldMapper(fields, field_map)
processed_data = mapper.process(data)
print(processed_data)
print(mapper.error)

```

4. Custom Validation
Define custom validation logic for specific fields.

```python
def validate_email(value):  
    import re  
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):  
        raise ValueError(f"Invalid email address: {value}")  

#Add the custom validator in the field definition:
field_map = {
    "name": "full_name",
    "email": "contact_email",
    "phone": "mobile_number",
    "income": "monthly_income"
}
fields = {
    "name": {"type": str, "max_length": 50, "required_field": True, "required_value":True},
    "email": {"type": str, "max_length": 100, "required_field": True, "required_value":True, "custom": validate_email},
    "phone": {"type": str, "max_length": 15, "required_field": False, "required_value":False},
    "income": {"type": int, "max_length": 15, "required_field": True, "required_value":False}
}

data = [
    {"name": "Alice", "email": "alice@example.com", "phone": "1234567890"},
    {"name": "Bob", "email": "charlieexample.com", "phone": "453543535", "income":0},
    {"name": "Charlie", "email": "charlie@example.com", "phone": "34534523", "income":0}
]
mapper = FieldMapper(fields, field_map)
processed_data = mapper.process(data)
print(processed_data)
print(mapper.error)

```

5. Optional Fields
Mark fields as optional with required_field: False. 
```python
fields = {
    "phone": {"type": str, "max_length": 15, "required_field": False},
}

```

6. Required Value
If required_value=True is set, their presence is mandatory and values can't be empty. 
```python
fields = {"email": {"type": str, "max_length": 100, "required_field": True, "required_value":True}

```

7. Skip Duplicates Data
If skip_duplicate=True is set, Skip duplicate data. Raises:DuplicatesDataError: If duplicate entries are found. 
```python
from field_mapper.mapper import FieldMapper

field_map = {
    "name": "full_name",
    "email": "contact_email",
    "phone": "mobile_number",
    "income": "monthly_income"
}
fields = {
    "name": {"type": str, "max_length": 50, "required_field": True, "required_value":True},
    "email": {"type": str, "max_length": 100, "required_field": True, "required_value":True},
    "phone": {"type": str, "max_length": 15, "required_field": False, "required_value":False},
    "income": {"type": int, "max_length": 15, "required_field": True, "required_value":False}
}
data = [
    {"name": "Charlie", "email": "charlie@example.com", "phone": "888888", "income":0},
    {"name": "Charlie", "email": "charlie@example.com", "phone": "444444", "income":0},
    {"name": "Charlie", "email": "charlie@example.com", "phone": "444444", "income":0}
]
mapper = FieldMapper(fields, field_map)
processed_data = mapper.process(data, skip_duplicate=True)
print("Output:", processed_data)
print("Error:",mapper.error)
```
8. Get Nested Data
```python
from field_mapper.mapper import FieldMapper

field_map = {
    "name": "full_name",
    "email[0]": "contact_email",
    "phone.phone_two": "mobile_number",
    "income[0].Jan": "monthly_income",
    "year_salary[].year": "salary"
}
data = [
    {
        "name": "Alice",
        "email": ["alice@example.com", "alice2@example.com"],
        "phone": {"phone_one": '22222', "phone_two": "2332432"},
        "income": [{"Jan": 2000, "Feb": 3000}],
        "year_salary": [
            {"year": "2020", "Jan": 2000, "Feb": 3000},
            {"year": "2021", "Jan": 2000, "Feb": 3000}
        ]
    }
]
fields = {
    "name": {"type": str, "position": "name", "max_length": 50, "required_field": True, "required_value": True},
    "email": {"type": list, "position": "email[0]", "max_length": 100, "required_field": True, "required_value": True},
    "phone": {"type": dict, "position": "phone.phone_two", "required_field": True, "required_value": True},
    "income": {"type": list, "position": "income[0].Jan", "required_field": True, "required_value": True},
    "year_salary": {"type": list, "position": "year_salary[].year", "required_field": True, "required_value": True}
}
mapper = FieldMapper(fields=fields, field_map=field_map)
processed_data = mapper.process(data, skip_duplicate=True)
print("Output:", processed_data)
print("Error:",mapper.error)

#Output: [{'full_name': 'Alice', 'contact_email': 'alice@example.com', 'mobile_number': '2332432', 'monthly_income': 2000, 'salary': ['2020', '2021']}]
#Error: []
```

### Example usage

```python
from field_mapper import FieldMapper


def validate_email(value: str) -> bool:
    return "@" in value and "." in value

field_map = {
    "name": "full_name",
    "email": "contact_email",
    "phone": "mobile_number",
    "income": "monthly_income"
}

fields = {
    "name": {"type": str, "max_length": 50, "required_field": True, "required_value":True},
    "email": {"type": str, "max_length": 100, "required_field": True, "required_value":True, "custom": validate_email},
    "phone": {"type": str, "max_length": 15, "required_field": False, "required_value":False},
    "income": {"type": int, "max_length": 15, "required_field": True, "required_value":False}
}

data = [
    {"name": "Alice", "email": "alice@example.com", "phone": "1234567890"},
    {"name": "Bob", "email": "charlieexample.com", "phone": "453543535", "income":0},
    {"name": "Charlie", "email": "charlie@example.com", "phone": "34534523", "income":0}
]
mapper = FieldMapper(fields, field_map)
processed_data = mapper.process(data)
print(processed_data)
print(mapper.error)
```

## Contributors
- [Md Lutfor Rahman](https://github.com/shifat151)
