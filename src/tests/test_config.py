"""
Tests for configuration module
"""

import unittest
import tempfile
import json
import os

from src.core.config import Config


class TestConfig(unittest.TestCase):
    """Test cases for Config class"""

    def setUp(self):
        """Set up test fixtures"""
        self.config = Config()

    def test_default_config(self):
        """Test default configuration values"""
        self.assertEqual(self.config.get("app_name"), "GRUB")
        self.assertEqual(self.config.get("version"), "1.0.0")
        self.assertFalse(self.config.get("debug"))

    def test_get_with_default(self):
        """Test get method with default value"""
        self.assertEqual(self.config.get("nonexistent", "default"), "default")

    def test_set_value(self):
        """Test setting configuration value"""
        self.config.set("test_key", "test_value")
        self.assertEqual(self.config.get("test_key"), "test_value")

    def test_load_from_file(self):
        """Test loading configuration from file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_config = {"test_key": "test_value", "debug": True}
            json.dump(test_config, f)
            temp_file = f.name

        try:
            config = Config(temp_file)
            self.assertEqual(config.get("test_key"), "test_value")
            self.assertTrue(config.get("debug"))
        finally:
            os.unlink(temp_file)

    def test_save_to_file(self):
        """Test saving configuration to file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name

        try:
            self.config.set("new_key", "new_value")
            self.config.save_to_file(temp_file)

            with open(temp_file, 'r') as f:
                saved_config = json.load(f)
                self.assertEqual(saved_config["new_key"], "new_value")
        finally:
            os.unlink(temp_file)

    def test_get_all(self):
        """Test getting all configuration values"""
        all_config = self.config.get_all()
        self.assertIsInstance(all_config, dict)
        self.assertIn("app_name", all_config)


if __name__ == '__main__':
    unittest.main()
