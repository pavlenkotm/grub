"""
Data validation utilities
"""

import re
from typing import Any, Dict, List, Optional


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class Validator:
    """Data validator with various validation methods"""

    @staticmethod
    def is_email(value: str) -> bool:
        """Validate email address

        Args:
            value: Email string to validate

        Returns:
            True if valid email
        """
        # More robust email validation
        # Local part: alphanumeric and ._%+- but no consecutive dots or dots at start/end
        # Domain: alphanumeric and dots/hyphens, at least one dot, valid TLD
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._%+-]*[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$|^[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$'

        if not re.match(pattern, value):
            return False

        # Additional checks for consecutive dots and other invalid patterns
        local, domain = value.rsplit('@', 1)

        # Check for consecutive dots
        if '..' in local or '..' in domain:
            return False

        # Check local part length (max 64 characters per RFC 5321)
        if len(local) > 64:
            return False

        # Check total length (max 254 characters per RFC 5321)
        if len(value) > 254:
            return False

        # Check domain part (max 253 characters)
        if len(domain) > 253:
            return False

        return True

    @staticmethod
    def is_url(value: str) -> bool:
        """Validate URL

        Args:
            value: URL string to validate

        Returns:
            True if valid URL
        """
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, value))

    @staticmethod
    def is_phone(value: str) -> bool:
        """Validate phone number (basic format)

        Args:
            value: Phone number string

        Returns:
            True if valid phone number
        """
        pattern = r'^\+?1?\d{9,15}$'
        return bool(re.match(pattern, value.replace(' ', '').replace('-', '')))

    @staticmethod
    def is_alphanumeric(value: str) -> bool:
        """Check if string is alphanumeric

        Args:
            value: String to check

        Returns:
            True if alphanumeric
        """
        return value.isalnum()

    @staticmethod
    def is_numeric(value: str) -> bool:
        """Check if string is numeric

        Args:
            value: String to check

        Returns:
            True if numeric
        """
        return value.isdigit()

    @staticmethod
    def is_in_range(value: float, min_val: float, max_val: float) -> bool:
        """Check if value is in range

        Args:
            value: Value to check
            min_val: Minimum value
            max_val: Maximum value

        Returns:
            True if in range
        """
        return min_val <= value <= max_val

    @staticmethod
    def min_length(value: str, length: int) -> bool:
        """Check minimum string length

        Args:
            value: String to check
            length: Minimum length

        Returns:
            True if meets minimum length
        """
        return len(value) >= length

    @staticmethod
    def max_length(value: str, length: int) -> bool:
        """Check maximum string length

        Args:
            value: String to check
            length: Maximum length

        Returns:
            True if within maximum length
        """
        return len(value) <= length

    @staticmethod
    def is_required(value: Any) -> bool:
        """Check if value is not None or empty

        Args:
            value: Value to check

        Returns:
            True if value exists
        """
        if value is None:
            return False
        if isinstance(value, str):
            return bool(value.strip())
        return True

    @staticmethod
    def matches_pattern(value: str, pattern: str) -> bool:
        """Check if value matches regex pattern

        Args:
            value: String to check
            pattern: Regex pattern

        Returns:
            True if matches pattern
        """
        return bool(re.match(pattern, value))

    @staticmethod
    def is_in_list(value: Any, allowed_values: List[Any]) -> bool:
        """Check if value is in allowed list

        Args:
            value: Value to check
            allowed_values: List of allowed values

        Returns:
            True if value in list
        """
        return value in allowed_values

    def validate_dict(self, data: Dict[str, Any], rules: Dict[str, List[Dict]]) -> Dict[str, List[str]]:
        """Validate dictionary against rules

        Args:
            data: Dictionary to validate
            rules: Validation rules for each field

        Returns:
            Dictionary of field: error_messages

        Example:
            rules = {
                'email': [
                    {'type': 'required'},
                    {'type': 'email'}
                ],
                'age': [
                    {'type': 'required'},
                    {'type': 'range', 'min': 0, 'max': 150}
                ]
            }
        """
        errors = {}

        for field, field_rules in rules.items():
            field_errors = []
            value = data.get(field)

            for rule in field_rules:
                rule_type = rule.get('type')

                if rule_type == 'required' and not self.is_required(value):
                    field_errors.append(f"{field} is required")
                elif value is not None:  # Skip other validations if value is None and not required
                    if rule_type == 'email' and not self.is_email(str(value)):
                        field_errors.append(f"{field} must be a valid email")
                    elif rule_type == 'url' and not self.is_url(str(value)):
                        field_errors.append(f"{field} must be a valid URL")
                    elif rule_type == 'phone' and not self.is_phone(str(value)):
                        field_errors.append(f"{field} must be a valid phone number")
                    elif rule_type == 'min_length':
                        min_len = rule.get('length', 0)
                        if not self.min_length(str(value), min_len):
                            field_errors.append(f"{field} must be at least {min_len} characters")
                    elif rule_type == 'max_length':
                        max_len = rule.get('length', 0)
                        if not self.max_length(str(value), max_len):
                            field_errors.append(f"{field} must be at most {max_len} characters")
                    elif rule_type == 'range':
                        min_val = rule.get('min', float('-inf'))
                        max_val = rule.get('max', float('inf'))
                        if not self.is_in_range(float(value), min_val, max_val):
                            field_errors.append(f"{field} must be between {min_val} and {max_val}")
                    elif rule_type == 'pattern':
                        pattern = rule.get('pattern', '')
                        if not self.matches_pattern(str(value), pattern):
                            field_errors.append(f"{field} does not match required pattern")
                    elif rule_type == 'in_list':
                        allowed = rule.get('values', [])
                        if not self.is_in_list(value, allowed):
                            field_errors.append(f"{field} must be one of: {', '.join(map(str, allowed))}")

            if field_errors:
                errors[field] = field_errors

        return errors
