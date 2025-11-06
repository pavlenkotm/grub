"""
Caching system module
"""

import time
from typing import Any, Dict, Optional
from threading import Lock

from .logger import get_logger


class Cache:
    """Simple in-memory cache with TTL support"""

    def __init__(self, default_ttl: int = 300):
        """Initialize cache

        Args:
            default_ttl: Default time-to-live in seconds
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
        self.default_ttl = default_ttl
        self.logger = get_logger()

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found or expired
        """
        with self._lock:
            if key not in self._cache:
                return None

            entry = self._cache[key]
            if entry['expires_at'] < time.time():
                del self._cache[key]
                self.logger.debug(f"Cache miss (expired): {key}")
                return None

            self.logger.debug(f"Cache hit: {key}")
            return entry['value']

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if not specified)
        """
        ttl = ttl if ttl is not None else self.default_ttl
        expires_at = time.time() + ttl

        with self._lock:
            self._cache[key] = {
                'value': value,
                'expires_at': expires_at,
                'created_at': time.time()
            }
            self.logger.debug(f"Cache set: {key} (TTL: {ttl}s)")

    def delete(self, key: str) -> bool:
        """Delete value from cache

        Args:
            key: Cache key

        Returns:
            True if key was deleted, False if not found
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                self.logger.debug(f"Cache delete: {key}")
                return True
            return False

    def clear(self) -> None:
        """Clear all cache entries"""
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            self.logger.info(f"Cache cleared ({count} entries)")

    def cleanup_expired(self) -> int:
        """Remove expired entries from cache

        Returns:
            Number of entries removed
        """
        current_time = time.time()
        expired_keys = []

        with self._lock:
            for key, entry in self._cache.items():
                if entry['expires_at'] < current_time:
                    expired_keys.append(key)

            for key in expired_keys:
                del self._cache[key]

        if expired_keys:
            self.logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")

        return len(expired_keys)

    def size(self) -> int:
        """Get number of entries in cache

        Returns:
            Number of cache entries
        """
        with self._lock:
            return len(self._cache)

    def keys(self) -> list:
        """Get all cache keys

        Returns:
            List of cache keys
        """
        with self._lock:
            return list(self._cache.keys())

    def has(self, key: str) -> bool:
        """Check if key exists and is not expired

        Args:
            key: Cache key

        Returns:
            True if key exists and is valid
        """
        return self.get(key) is not None


# Global cache instance
_default_cache: Optional[Cache] = None


def get_cache(default_ttl: int = 300) -> Cache:
    """Get or create default cache instance

    Args:
        default_ttl: Default time-to-live in seconds

    Returns:
        Cache instance
    """
    global _default_cache
    if _default_cache is None:
        _default_cache = Cache(default_ttl)
    return _default_cache
