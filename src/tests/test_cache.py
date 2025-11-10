"""
Tests for cache module
"""

import time
import unittest
from src.utils.cache import Cache


class TestCache(unittest.TestCase):
    """Test cases for Cache class"""

    def setUp(self):
        """Set up test fixtures"""
        self.cache = Cache(default_ttl=2, max_size=3)

    def test_set_and_get(self):
        """Test setting and getting cache values"""
        self.cache.set("key1", "value1")
        self.assertEqual(self.cache.get("key1"), "value1")

    def test_get_nonexistent(self):
        """Test getting nonexistent key"""
        self.assertIsNone(self.cache.get("nonexistent"))

    def test_ttl_expiration(self):
        """Test TTL expiration"""
        self.cache.set("key1", "value1", ttl=1)
        self.assertEqual(self.cache.get("key1"), "value1")
        time.sleep(1.5)
        self.assertIsNone(self.cache.get("key1"))

    def test_delete(self):
        """Test deleting cache entries"""
        self.cache.set("key1", "value1")
        self.assertTrue(self.cache.delete("key1"))
        self.assertIsNone(self.cache.get("key1"))
        self.assertFalse(self.cache.delete("key1"))

    def test_clear(self):
        """Test clearing all cache entries"""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.clear()
        self.assertEqual(self.cache.size(), 0)

    def test_size(self):
        """Test cache size tracking"""
        self.assertEqual(self.cache.size(), 0)
        self.cache.set("key1", "value1")
        self.assertEqual(self.cache.size(), 1)
        self.cache.set("key2", "value2")
        self.assertEqual(self.cache.size(), 2)

    def test_lru_eviction(self):
        """Test LRU eviction when max_size is reached"""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        # Cache is now full (max_size=3)

        # Access key1 to make it recently used
        self.cache.get("key1")

        # Add key4, should evict key2 (least recently used)
        self.cache.set("key4", "value4")

        self.assertIsNone(self.cache.get("key2"))  # key2 was evicted
        self.assertIsNotNone(self.cache.get("key1"))  # key1 still exists
        self.assertIsNotNone(self.cache.get("key3"))
        self.assertIsNotNone(self.cache.get("key4"))

    def test_cleanup_expired(self):
        """Test cleanup of expired entries"""
        self.cache.set("key1", "value1", ttl=1)
        self.cache.set("key2", "value2", ttl=10)
        time.sleep(1.5)
        count = self.cache.cleanup_expired()
        self.assertEqual(count, 1)
        self.assertIsNone(self.cache.get("key1"))
        self.assertIsNotNone(self.cache.get("key2"))

    def test_has(self):
        """Test checking key existence"""
        self.cache.set("key1", "value1")
        self.assertTrue(self.cache.has("key1"))
        self.assertFalse(self.cache.has("key2"))

    def test_keys(self):
        """Test getting all cache keys"""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        keys = self.cache.keys()
        self.assertIn("key1", keys)
        self.assertIn("key2", keys)
        self.assertEqual(len(keys), 2)

    def test_stats(self):
        """Test cache statistics"""
        self.cache.set("key1", "value1")
        self.cache.get("key1")  # hit
        self.cache.get("key2")  # miss

        stats = self.cache.get_stats()
        self.assertEqual(stats['size'], 1)
        self.assertEqual(stats['hits'], 1)
        self.assertEqual(stats['misses'], 1)
        self.assertEqual(stats['max_size'], 3)


if __name__ == '__main__':
    unittest.main()
