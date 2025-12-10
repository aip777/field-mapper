"""
Production-Ready Test Scenarios for Field Mapper

This test suite covers all real-world usage scenarios to ensure
the library is production-ready.

Test Categories:
1. API Integration Scenarios
2. Database Import/Export Scenarios
3. CSV/Excel Data Processing
4. Microservices Data Transformation
5. Form Validation Scenarios
6. Edge Cases and Error Handling
7. Performance and Scale Testing
8. Real-World Business Logic
"""

import unittest
from field_mapper import FieldMapper
from field_mapper.exc.exception import FieldValidationError, DuplicateDataError


class TestAPIIntegrationScenarios(unittest.TestCase):
    """Test scenarios for API data integration."""

    def test_rest_api_response_transformation(self):
        """Test transforming REST API response to internal format."""
        fields = {
            "firstName": {"type": str, "max_length": 50},
            "lastName": {"type": str, "max_length": 50},
            "emailAddress": {"type": str, "max_length": 100},
            "phoneNumber": {"type": str, "required_field": False},
            "isActive": {"type": bool}
        }
        field_map = {
            "firstName": "first_name",
            "lastName": "last_name",
            "emailAddress": "email",
            "phoneNumber": "phone",
            "isActive": "active"
        }

        api_data = [{
            "firstName": "John",
            "lastName": "Doe",
            "emailAddress": "john.doe@example.com",
            "phoneNumber": "555-1234",
            "isActive": True
        }]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(api_data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["first_name"], "John")
        self.assertEqual(result[0]["email"], "john.doe@example.com")
        self.assertTrue(result[0]["active"])

    def test_nested_json_api_response(self):
        """Test extracting data from nested JSON API responses."""
        fields = {
            "user": {"type": dict, "position": "user.profile.name", "required_field": True},
            "contacts": {"type": list, "position": "user.contacts[0].value", "required_field": False}
        }
        field_map = {
            "user.profile.name": "username",
            "user.contacts[0].value": "primary_email"
        }

        api_data = [{
            "user": {
                "id": 123,
                "profile": {
                    "name": "Alice",
                    "bio": "Developer"
                },
                "contacts": [
                    {"type": "email", "value": "alice@example.com"}
                ]
            }
        }]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(api_data)
        print(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["username"], "Alice")
        self.assertEqual(result[0]["primary_email"], "alice@example.com")

    def test_third_party_api_with_optional_fields(self):
        """Test handling third-party APIs with optional/missing fields."""
        fields = {
            "id": {"type": int, "required_field": True},
            "name": {"type": str, "required_field": True},
            "description": {"type": str, "required_field": False, "required_value": False},
            "tags": {"type": list, "required_field": False, "required_value": False}
        }
        field_map = {"id": "user_id", "name": "username", "description": "bio", "tags": "labels"}

        api_data = [
            {"id": 1, "name": "Alice", "description": "Dev", "tags": ["python"]},
            {"id": 2, "name": "Bob"},
            {"id": 3, "name": "Charlie", "description": "", "tags": []}
        ]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(api_data)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[1]["bio"], None)
        self.assertEqual(result[2]["labels"], [])


class TestDatabaseScenarios(unittest.TestCase):
    """Test scenarios for database operations."""

    def test_database_import_validation(self):
        """Test validating data before database import."""
        def validate_email(email):
            import re
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(pattern, email))

        def validate_age(age):
            return 0 <= age <= 150

        fields = {
            "email": {"type": str, "max_length": 255, "custom": validate_email},
            "age": {"type": int, "custom": validate_age},
            "username": {"type": str, "max_length": 50},
            "created_at": {"type": str, "required_field": False}
        }
        field_map = {"email": "email", "age": "age", "username": "username", "created_at": "created_at"}

        import_data = [
            {"email": "valid@example.com", "age": 25, "username": "user1"},
            {"email": "invalid-email", "age": 30, "username": "user2"}
        ]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(import_data)

        self.assertEqual(len(result), 0)
        self.assertTrue(mapper.error)

    def test_csv_to_database_transformation(self):
        """Test transforming CSV data format to database schema."""
        fields = {
            "Name": {"type": str, "max_length": 100},
            "Email": {"type": str, "max_length": 255},
            "Phone": {"type": str, "required_field": False},
            "Department": {"type": str, "max_length": 50}
        }
        field_map = {
            "Name": "employee_name",
            "Email": "employee_email",
            "Phone": "contact_number",
            "Department": "dept_name"
        }

        csv_data = [
            {"Name": "John Smith", "Email": "john@company.com", "Phone": "555-0001", "Department": "Engineering"},
            {"Name": "Jane Doe", "Email": "jane@company.com", "Department": "Sales"}
        ]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(csv_data)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["dept_name"], "Engineering")
        self.assertIsNone(result[1]["contact_number"])

    def test_duplicate_prevention_for_database(self):
        """Test preventing duplicate entries before database insert."""
        fields = {
            "user_id": {"type": int},
            "email": {"type": str}
        }
        field_map = {"user_id": "id", "email": "email"}

        data = [
            {"user_id": 1, "email": "alice@example.com"},
            {"user_id": 2, "email": "bob@example.com"},
            {"user_id": 1, "email": "alice@example.com"}
        ]

        mapper = FieldMapper(fields, field_map)

        with self.assertRaises(DuplicateDataError):
            from field_mapper.mapper import DuplicateDataHandler
            DuplicateDataHandler().remove_duplicates(data)


class TestFormValidationScenarios(unittest.TestCase):
    """Test scenarios for web form validation."""

    def test_user_registration_form(self):
        """Test validating user registration form data."""
        def validate_password(pwd):
            if len(pwd) < 8:
                raise ValueError("Password must be at least 8 characters")
            if not any(c.isupper() for c in pwd):
                raise ValueError("Password must contain uppercase letter")
            if not any(c.isdigit() for c in pwd):
                raise ValueError("Password must contain digit")
            return True

        def validate_email(email):
            return "@" in email and "." in email

        fields = {
            "username": {"type": str, "max_length": 30, "required_value": True},
            "email": {"type": str, "max_length": 255, "custom": validate_email},
            "password": {"type": str, "max_length": 128, "custom": validate_password},
            "age": {"type": int, "required_field": False},
            "terms_accepted": {"type": bool, "required_value": True}
        }
        field_map = {
            "username": "username",
            "email": "email",
            "password": "password",
            "age": "age",
            "terms_accepted": "terms"
        }

        valid_form = [{
            "username": "johndoe",
            "email": "john@example.com",
            "password": "SecurePass123",
            "terms_accepted": True
        }]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(valid_form)

        self.assertEqual(len(result), 1)
        self.assertTrue(result[0]["terms"])

    def test_contact_form_with_optional_fields(self):
        """Test contact form with mix of required and optional fields."""
        fields = {
            "name": {"type": str, "max_length": 100, "required_value": True},
            "email": {"type": str, "max_length": 255, "required_value": True},
            "phone": {"type": str, "required_field": False, "required_value": False},
            "message": {"type": str, "max_length": 1000, "required_value": True},
            "subscribe": {"type": bool, "required_field": False}
        }
        field_map = {
            "name": "contact_name",
            "email": "contact_email",
            "phone": "contact_phone",
            "message": "message_text",
            "subscribe": "newsletter_opt_in"
        }

        form_data = [
            {
                "name": "Alice",
                "email": "alice@example.com",
                "message": "Hello, I need help with...",
                "subscribe": True
            }
        ]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(form_data)

        self.assertEqual(len(result), 1)
        self.assertIsNone(result[0]["contact_phone"])
        self.assertTrue(result[0]["newsletter_opt_in"])


class TestMicroservicesScenarios(unittest.TestCase):
    """Test scenarios for microservices data transformation."""

    def test_service_to_service_communication(self):
        """Test transforming data between microservices."""
        fields = {
            "orderId": {"type": str, "max_length": 50},
            "customerId": {"type": int},
            "items": {"type": list, "position": "items[].productId"},
            "totalAmount": {"type": float}
        }
        field_map = {
            "orderId": "order_id",
            "customerId": "customer_id",
            "items[].productId": "product_ids",
            "totalAmount": "total"
        }

        service_data = [{
            "orderId": "ORD-12345",
            "customerId": 456,
            "items": [
                {"productId": "PROD-1", "quantity": 2},
                {"productId": "PROD-2", "quantity": 1}
            ],
            "totalAmount": 99.99
        }]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(service_data)

        self.assertEqual(result[0]["order_id"], "ORD-12345")
        self.assertEqual(result[0]["product_ids"], ["PROD-1", "PROD-2"])

    def test_event_driven_data_transformation(self):
        """Test transforming event data for message queues."""
        fields = {
            "eventType": {"type": str, "max_length": 50},
            "timestamp": {"type": str},
            "payload": {"type": dict}
        }
        field_map = {
            "eventType": "event_name",
            "timestamp": "event_time",
            "payload": "event_data"
        }

        event_data = [{
            "eventType": "USER_LOGGED_IN",
            "timestamp": "2024-01-01T10:00:00Z",
            "payload": {
                "data": {
                    "userId": 123,
                    "sessionId": "sess-456"
                }
            }
        }]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(event_data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["event_name"], "USER_LOGGED_IN")
        self.assertEqual(result[0]["event_data"]["data"]["userId"], 123)


class TestEdgeCasesAndErrorHandling(unittest.TestCase):
    """Test edge cases and error scenarios."""

    def test_empty_data_list(self):
        """Test processing empty data list."""
        fields = {"name": {"type": str}}
        field_map = {"name": "name"}

        mapper = FieldMapper(fields, field_map)
        result = mapper.process([])

        self.assertEqual(len(result), 0)
        self.assertFalse(mapper.error)

    def test_single_record(self):
        """Test processing single record."""
        fields = {"name": {"type": str}}
        field_map = {"name": "username"}

        mapper = FieldMapper(fields, field_map)
        result = mapper.process([{"name": "Alice"}])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["username"], "Alice")

    def test_very_long_strings(self):
        """Test validation with very long strings."""
        fields = {"description": {"type": str, "max_length": 1000}}
        field_map = {"description": "desc"}

        long_text = "a" * 1001
        data = [{"description": long_text}]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)

        self.assertEqual(len(result), 0)
        self.assertTrue(mapper.error)

    def test_unicode_and_special_characters(self):
        """Test handling unicode and special characters."""
        fields = {
            "name": {"type": str, "max_length": 100},
            "description": {"type": str, "max_length": 500}
        }
        field_map = {"name": "name", "description": "desc"}

        data = [{
            "name": "José García",
            "description": "Special chars: !@#$%^&*()_+-=[]{}|;':\"<>?,./~`"
        }]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "José García")

    def test_null_vs_empty_values(self):
        """Test distinction between null and empty values."""
        fields = {
            "name": {"type": str, "required_value": True},
            "bio": {"type": str, "required_value": False},
            "tags": {"type": list, "required_value": False}
        }
        field_map = {"name": "name", "bio": "bio", "tags": "tags"}

        data = [
            {"name": "Alice", "bio": "", "tags": []},
            {"name": "Bob", "bio": None, "tags": None}
        ]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["bio"], "")
        self.assertIsNone(result[1]["bio"])

    def test_numeric_edge_cases(self):
        """Test numeric edge cases (zero, negative, large numbers)."""
        fields = {
            "count": {"type": int, "required_value": False},
            "price": {"type": float, "required_value": False},
            "quantity": {"type": int, "required_value": False}
        }
        field_map = {"count": "count", "price": "price", "quantity": "qty"}

        data = [{
            "count": 0,
            "price": -99.99,
            "quantity": 999999999
        }]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["count"], 0)
        self.assertEqual(result[0]["price"], -99.99)

    def test_boolean_edge_cases(self):
        """Test boolean values in various contexts."""
        fields = {
            "is_active": {"type": bool, "required_value": False},
            "is_admin": {"type": bool, "required_value": False},
            "email_verified": {"type": bool, "required_value": True}
        }
        field_map = {
            "is_active": "active",
            "is_admin": "admin",
            "email_verified": "verified"
        }

        data = [{
            "is_active": False,
            "is_admin": True,
            "email_verified": False
        }]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)

        self.assertEqual(len(result), 1)
        self.assertFalse(result[0]["active"])
        self.assertTrue(result[0]["admin"])

    def test_deeply_nested_data(self):
        """Test extraction from deeply nested structures."""
        fields = {
            "response": {"type": dict}
        }
        field_map = {
            "response.data.user.profile.contact.email": "user_email"
        }

        data = [{
            "response": {
                "data": {
                    "user": {
                        "profile": {
                            "contact": {
                                "email": "deep@example.com"
                            }
                        }
                    }
                }
            }
        }]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["user_email"], "deep@example.com")

    def test_mixed_data_types_in_list(self):
        """Test handling lists with mixed types."""
        fields = {
            "values": {"type": list, "max_length": 10}
        }
        field_map = {"values": "data"}

        data = [{
            "values": [1, "two", 3.0, True, None, {"key": "value"}]
        }]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(data)

        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]["data"]), 6)


class TestRealWorldBusinessLogic(unittest.TestCase):
    """Test real-world business validation scenarios."""

    def test_ecommerce_order_validation(self):
        """Test e-commerce order validation with business rules."""
        def validate_order_total(total):
            return total >= 0

        def validate_email(email):
            return "@" in email

        fields = {
            "orderId": {"type": str, "max_length": 50},
            "customerEmail": {"type": str, "custom": validate_email},
            "items": {"type": list, "max_length": 100},
            "totalAmount": {"type": float, "custom": validate_order_total},
            "shippingAddress": {"type": dict},
            "paymentMethod": {"type": str, "max_length": 50}
        }
        field_map = {
            "orderId": "order_id",
            "customerEmail": "customer_email",
            "items": "order_items",
            "totalAmount": "total",
            "shippingAddress": "shipping_addr",
            "paymentMethod": "payment"
        }

        order_data = [{
            "orderId": "ORD-2024-001",
            "customerEmail": "customer@example.com",
            "items": [{"sku": "ITEM-1", "qty": 2}],
            "totalAmount": 149.99,
            "shippingAddress": {"street": "123 Main St", "city": "NYC"},
            "paymentMethod": "credit_card"
        }]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(order_data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["order_id"], "ORD-2024-001")

    def test_employee_data_with_department_hierarchy(self):
        """Test employee data with hierarchical department structure."""
        fields = {
            "employee": {"type": dict}
        }
        field_map = {
            "employee.personal.fullName": "name",
            "employee.work.department.name": "dept",
            "employee.compensation[0].amount": "current_salary"
        }

        employee_data = [{
            "employee": {
                "personal": {"fullName": "John Smith"},
                "work": {
                    "department": {
                        "name": "Engineering",
                        "code": "ENG"
                    }
                },
                "compensation": [
                    {"year": 2024, "amount": 120000}
                ]
            }
        }]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(employee_data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "John Smith")
        self.assertEqual(result[0]["dept"], "Engineering")
        self.assertEqual(result[0]["current_salary"], 120000)

    def test_inventory_management_validation(self):
        """Test inventory management data validation."""
        def validate_sku(sku):
            return len(sku) >= 5 and sku.startswith("SKU-")

        def validate_quantity(qty):
            return qty >= 0

        fields = {
            "sku": {"type": str, "max_length": 50, "custom": validate_sku},
            "quantity": {"type": int, "custom": validate_quantity},
            "location": {"type": str, "max_length": 100},
            "price": {"type": float},
            "reorderLevel": {"type": int, "required_field": False}
        }
        field_map = {
            "sku": "product_sku",
            "quantity": "stock_qty",
            "location": "warehouse_location",
            "price": "unit_price",
            "reorderLevel": "reorder_threshold"
        }

        inventory_data = [{
            "sku": "SKU-12345",
            "quantity": 100,
            "location": "Warehouse A",
            "price": 29.99,
            "reorderLevel": 20
        }]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(inventory_data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["stock_qty"], 100)


class TestPerformanceScenarios(unittest.TestCase):
    """Test performance with large datasets."""

    def test_large_dataset_processing(self):
        """Test processing moderately large dataset."""
        fields = {
            "id": {"type": int},
            "name": {"type": str, "max_length": 100},
            "email": {"type": str, "max_length": 255}
        }
        field_map = {"id": "user_id", "name": "username", "email": "email"}

        large_data = [
            {"id": i, "name": f"User{i}", "email": f"user{i}@example.com"}
            for i in range(1000)
        ]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(large_data)

        self.assertEqual(len(result), 1000)
        self.assertEqual(result[0]["user_id"], 0)
        self.assertEqual(result[999]["user_id"], 999)

    def test_complex_nested_structure_performance(self):
        """Test performance with complex nested structures."""
        fields = {
            "data": {"type": dict}
        }
        field_map = {"data.users[0].profile.name": "first_user_name"}

        complex_data = [{
            "data": {
                "users": [
                    {
                        "id": i,
                        "profile": {
                            "name": f"User{i}",
                            "metadata": {"key": "value"}
                        }
                    }
                    for i in range(100)
                ]
            }
        }]

        mapper = FieldMapper(fields, field_map)
        result = mapper.process(complex_data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["first_user_name"], "User0")


if __name__ == "__main__":
    unittest.main()