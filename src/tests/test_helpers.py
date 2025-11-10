"""
Tests for helper utility functions
"""

import unittest
from src.utils.helpers import (
    get_timestamp,
    calculate_hash,
    chunk_list,
    sanitize_filename,
    format_size
)


class TestHelpers(unittest.TestCase):
    """Test cases for helper functions"""

    def test_get_timestamp(self):
        """Test timestamp generation"""
        timestamp = get_timestamp()
        self.assertIsInstance(timestamp, str)
        self.assertIn("-", timestamp)
        self.assertIn(":", timestamp)

    def test_calculate_hash_sha256(self):
        """Test SHA256 hash calculation"""
        data = "test data"
        hash_value = calculate_hash(data, "sha256")
        self.assertIsInstance(hash_value, str)
        self.assertEqual(len(hash_value), 64)  # SHA256 produces 64 hex characters

    def test_calculate_hash_md5(self):
        """Test MD5 hash calculation"""
        data = "test data"
        hash_value = calculate_hash(data, "md5")
        self.assertIsInstance(hash_value, str)
        self.assertEqual(len(hash_value), 32)  # MD5 produces 32 hex characters

    def test_chunk_list(self):
        """Test list chunking"""
        items = list(range(10))
        chunks = chunk_list(items, 3)
        self.assertEqual(len(chunks), 4)
        self.assertEqual(chunks[0], [0, 1, 2])
        self.assertEqual(chunks[-1], [9])

    def test_sanitize_filename(self):
        """Test filename sanitization"""
        filename = 'test<file>name:with*invalid?chars.txt'
        sanitized = sanitize_filename(filename)
        self.assertNotIn('<', sanitized)
        self.assertNotIn('>', sanitized)
        self.assertNotIn(':', sanitized)
        self.assertNotIn('*', sanitized)
        self.assertNotIn('?', sanitized)

    def test_format_size(self):
        """Test size formatting"""
        self.assertIn("B", format_size(500))
        self.assertIn("KB", format_size(1024))
        self.assertIn("MB", format_size(1024 * 1024))
        self.assertIn("GB", format_size(1024 * 1024 * 1024))


if __name__ == '__main__':
    unittest.main()
