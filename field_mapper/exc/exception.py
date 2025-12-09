from typing import Any


class FieldValidationError(Exception):
    """
    Base exception for field validation errors.

    Attributes:
        issues: List of validation error messages
        problematic_data: The data that failed validation
    """
    def __init__(self, message: str, issues: Any = None, problematic_data: Any = None):
        super().__init__(message)
        self.issues = issues if issues is not None else []
        self.problematic_data = problematic_data


class DuplicateDataError(FieldValidationError):
    """Exception raised when duplicate data entries are detected."""
    pass

