"""
Tests for validator module
"""

import unittest
from src.utils.validator import Validator


class TestValidator(unittest.TestCase):
    """Test cases for Validator class"""

    def setUp(self):
        """Set up test fixtures"""
        self.validator = Validator()

    def test_is_email_valid(self):
        """Test valid email addresses"""
        valid_emails = [
            "test@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
            "a@example.com",
            "user123@test-domain.com"
        ]
        for email in valid_emails:
            self.assertTrue(self.validator.is_email(email), f"Should accept: {email}")

    def test_is_email_invalid(self):
        """Test invalid email addresses"""
        invalid_emails = [
            "test..email@example.com",  # consecutive dots
            ".test@example.com",  # starts with dot
            "test.@example.com",  # ends with dot
            "@example.com",  # no local part
            "test@",  # no domain
            "test",  # no @ symbol
            "test@.com",  # domain starts with dot
            "a" * 65 + "@example.com",  # local part too long
            "test@" + "a" * 250 + ".com"  # domain too long
        ]
        for email in invalid_emails:
            self.assertFalse(self.validator.is_email(email), f"Should reject: {email}")

    def test_is_url_valid(self):
        """Test valid URLs"""
        valid_urls = [
            "http://example.com",
            "https://www.example.com",
            "https://example.com/path/to/page",
            "http://example.com:8080"
        ]
        for url in valid_urls:
            self.assertTrue(self.validator.is_url(url), f"Should accept: {url}")

    def test_is_phone_valid(self):
        """Test valid phone numbers"""
        valid_phones = [
            "1234567890",
            "+1234567890",
            "+12345678901234",
            "123-456-7890",
            "123 456 7890"
        ]
        for phone in valid_phones:
            self.assertTrue(self.validator.is_phone(phone), f"Should accept: {phone}")

    def test_is_alphanumeric(self):
        """Test alphanumeric validation"""
        self.assertTrue(self.validator.is_alphanumeric("abc123"))
        self.assertFalse(self.validator.is_alphanumeric("abc-123"))
        self.assertFalse(self.validator.is_alphanumeric("abc 123"))

    def test_is_numeric(self):
        """Test numeric validation"""
        self.assertTrue(self.validator.is_numeric("12345"))
        self.assertFalse(self.validator.is_numeric("123.45"))
        self.assertFalse(self.validator.is_numeric("abc"))

    def test_is_in_range(self):
        """Test range validation"""
        self.assertTrue(self.validator.is_in_range(5, 1, 10))
        self.assertTrue(self.validator.is_in_range(1, 1, 10))
        self.assertTrue(self.validator.is_in_range(10, 1, 10))
        self.assertFalse(self.validator.is_in_range(0, 1, 10))
        self.assertFalse(self.validator.is_in_range(11, 1, 10))

    def test_min_length(self):
        """Test minimum length validation"""
        self.assertTrue(self.validator.min_length("hello", 3))
        self.assertTrue(self.validator.min_length("hello", 5))
        self.assertFalse(self.validator.min_length("hello", 6))

    def test_max_length(self):
        """Test maximum length validation"""
        self.assertTrue(self.validator.max_length("hello", 10))
        self.assertTrue(self.validator.max_length("hello", 5))
        self.assertFalse(self.validator.max_length("hello", 4))

    def test_is_required(self):
        """Test required field validation"""
        self.assertTrue(self.validator.is_required("value"))
        self.assertFalse(self.validator.is_required(None))
        self.assertFalse(self.validator.is_required(""))
        self.assertFalse(self.validator.is_required("   "))

    def test_matches_pattern(self):
        """Test pattern matching"""
        self.assertTrue(self.validator.matches_pattern("abc123", r'^[a-z]+\d+$'))
        self.assertFalse(self.validator.matches_pattern("123abc", r'^[a-z]+\d+$'))

    def test_is_in_list(self):
        """Test list membership validation"""
        allowed = ["red", "green", "blue"]
        self.assertTrue(self.validator.is_in_list("red", allowed))
        self.assertFalse(self.validator.is_in_list("yellow", allowed))

    def test_validate_dict(self):
        """Test dictionary validation"""
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

        # Valid data
        data = {'email': 'test@example.com', 'age': 25}
        errors = self.validator.validate_dict(data, rules)
        self.assertEqual(len(errors), 0)

        # Invalid email
        data = {'email': 'invalid-email', 'age': 25}
        errors = self.validator.validate_dict(data, rules)
        self.assertIn('email', errors)

        # Missing required field
        data = {'email': 'test@example.com'}
        errors = self.validator.validate_dict(data, rules)
        self.assertIn('age', errors)

        # Out of range
        data = {'email': 'test@example.com', 'age': 200}
        errors = self.validator.validate_dict(data, rules)
        self.assertIn('age', errors)


if __name__ == '__main__':
    unittest.main()
