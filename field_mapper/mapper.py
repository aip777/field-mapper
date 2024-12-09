from typing import List, Dict, Any, Callable, Union, Type

from field_mapper.exc.exception import FieldValidationError, MissingFieldError, InvalidTypeError, InvalidLengthError, \
    CustomValidationError, DuplicatesDataError


class FieldMapper:
    def __init__(self, fields: Dict[str, Dict[str, Union[Type, int, Callable, bool]]], field_map: Dict[str, str]):
        self.fields = fields
        self.field_map = field_map
        self.error = []

    def validate(self, data: Dict[str, Any]) -> None:
        """
        Validate fields based on the constraints provided in the `fields` dictionary.
        """

        errors = []
        for field, constraints in self.fields.items():
            is_required_field = constraints.get("required_field", True)
            is_required_value = constraints.get("required_value", True)
            expected_type = constraints.get("type")
            max_length = constraints.get("max_length")
            custom_validator = constraints.get("custom")
            value = data.get(field)

            # Check for missing fields
            if is_required_field and field not in data:
                errors.append(f"Missing required field: {field}")
                continue

            # Skip validation for optional fields if not present
            if not is_required_field and value is None:
                continue

            # Check if the value is missing when required
            if is_required_value and not value and value != 0:
                errors.append(f"Required value missing or invalid for field: {field}")

            # Validate type
            if value is not None and expected_type and not isinstance(value, expected_type):
                errors.append(f"Invalid type for field: {field}")

            # Validate max length for strings
            if value is not None and max_length and isinstance(value, str) and len(value) > max_length:
                errors.append(f"Field '{field}' exceeds max length of {max_length} characters")

            # Apply custom validation if defined
            if value is not None and custom_validator and callable(custom_validator):
                try:
                    if not custom_validator(value):
                        errors.append(f"Custom validation failed for field: {field}")
                except Exception as e:
                    errors.append(f"Error during custom validation for field: {field} ({str(e)})")

        if errors:
            raise FieldValidationError("Validation errors occurred", errors, [data])

    def map(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map internal fields to the target field names.
        """
        return {
            self.field_map.get(key, key): value
            for key, value in data.items()
            if key in self.field_map
        }

    def process(self, data: List[Dict[str, Any]], skip_duplicate: bool = False) -> List[Dict[str, Any]]:
        """
        Process a list of data entries, validating and mapping fields.
        """
        if not isinstance(data, list):
            raise ValueError("Input data must be a list of dictionaries.")

        if skip_duplicate:
            try:
                data = DuplicateDataHandler().remove_duplicates(data)
                result = []
                for entry in data:
                    self.validate(entry)
                    mapped_data = self.map(entry)
                    result.append(mapped_data)
                return result

            except FieldValidationError as exc:
                self._log_error(exc)
        else:
            result = []
            for entry in data:
                try:
                    self.validate(entry)
                    mapped_data = self.map(entry)
                    result.append(mapped_data)
                except FieldValidationError as exc:
                    self._log_error(exc)
            return result

    def _log_error(self, exc: FieldValidationError) -> None:
        """
        Log validation error details.
        """
        formatted_issues = "; ".join(exc.issues)  # Join issues into a single line
        formatted_error = (
            f"--- Error Details ---\n"
            f"Type: {exc.__class__.__name__}\n"
            f"Message: {formatted_issues}\n"
            f"Data: {exc.problematic_data}\n"
            f"---------------------"
        )
        self.error.append(formatted_error)
        print(formatted_error)


class DuplicateDataHandler:
    """Handles operations related to duplicate detection in data."""

    def _convert_to_hashable(self, obj: Any) -> Any:
        """Recursively converts mutable structures into immutable ones."""
        if isinstance(obj, dict):
            return frozenset((key, self._convert_to_hashable(value)) for key, value in obj.items())
        elif isinstance(obj, list):
            return tuple(self._convert_to_hashable(item) for item in obj)
        return obj

    def remove_duplicates(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Removes duplicate entries from the provided data list."""
        seen_hashes = set()
        unique_entries = []
        duplicate_entries = []

        for entry in data:
            entry_hashable = self._convert_to_hashable(entry)
            if entry_hashable in seen_hashes:
                duplicate_entries.append(entry)
            else:
                seen_hashes.add(entry_hashable)
                unique_entries.append(entry)

        if duplicate_entries:
            message = 'Duplicate data detected'
            raise DuplicatesDataError(message,[message], problematic_data=duplicate_entries)

        return unique_entries
