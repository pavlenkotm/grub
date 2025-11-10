"""
Tests for database module
"""

import unittest
import os
from src.core.database import Database


class TestDatabase(unittest.TestCase):
    """Test cases for Database class"""

    def setUp(self):
        """Set up test fixtures"""
        self.db = Database(":memory:")
        self.db.connect()

    def tearDown(self):
        """Clean up after tests"""
        self.db.disconnect()

    def test_create_table(self):
        """Test creating a table"""
        columns = {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT NOT NULL",
            "age": "INTEGER"
        }
        self.db.create_table("users", columns)
        # Verify table exists
        result = self.db.fetch_one("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        self.assertIsNotNone(result)

    def test_insert(self):
        """Test inserting data"""
        columns = {"id": "INTEGER PRIMARY KEY", "name": "TEXT"}
        self.db.create_table("users", columns)

        row_id = self.db.insert("users", {"name": "John"})
        self.assertIsNotNone(row_id)

        result = self.db.fetch_one("SELECT * FROM users WHERE id = ?", (row_id,))
        self.assertEqual(result['name'], "John")

    def test_update(self):
        """Test updating data"""
        columns = {"id": "INTEGER PRIMARY KEY", "name": "TEXT"}
        self.db.create_table("users", columns)

        row_id = self.db.insert("users", {"name": "John"})
        count = self.db.update("users", {"name": "Jane"}, "id = ?", (row_id,))

        self.assertEqual(count, 1)
        result = self.db.fetch_one("SELECT * FROM users WHERE id = ?", (row_id,))
        self.assertEqual(result['name'], "Jane")

    def test_delete(self):
        """Test deleting data"""
        columns = {"id": "INTEGER PRIMARY KEY", "name": "TEXT"}
        self.db.create_table("users", columns)

        row_id = self.db.insert("users", {"name": "John"})
        count = self.db.delete("users", "id = ?", (row_id,))

        self.assertEqual(count, 1)
        result = self.db.fetch_one("SELECT * FROM users WHERE id = ?", (row_id,))
        self.assertIsNone(result)

    def test_fetch_all(self):
        """Test fetching all rows"""
        columns = {"id": "INTEGER PRIMARY KEY", "name": "TEXT"}
        self.db.create_table("users", columns)

        self.db.insert("users", {"name": "John"})
        self.db.insert("users", {"name": "Jane"})
        self.db.insert("users", {"name": "Bob"})

        results = self.db.fetch_all("SELECT * FROM users")
        self.assertEqual(len(results), 3)

    def test_execute_many(self):
        """Test executing query with multiple parameter sets"""
        columns = {"id": "INTEGER PRIMARY KEY", "name": "TEXT"}
        self.db.create_table("users", columns)

        params = [("John",), ("Jane",), ("Bob",)]
        self.db.execute_many("INSERT INTO users (name) VALUES (?)", params)

        results = self.db.fetch_all("SELECT * FROM users")
        self.assertEqual(len(results), 3)


if __name__ == '__main__':
    unittest.main()
