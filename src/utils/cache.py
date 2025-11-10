"""
Caching system module
"""

import time
from typing import Any, Dict, Optional
from threading import Lock

from .logger import get_logger


class Cache:
    """Simple in-memory cache with TTL support and LRU eviction"""

    def __init__(self, default_ttl: int = 300, max_size: int = 1000):
        """Initialize cache

        Args:
            default_ttl: Default time-to-live in seconds
            max_size: Maximum number of entries (0 for unlimited)
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._access_order: Dict[str, float] = {}  # Track access times for LRU
        self._lock = Lock()
        self.default_ttl = default_ttl
        self.max_size = max_size
        self.logger = get_logger()
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found or expired
        """
        with self._lock:
            if key not in self._cache:
                self._misses += 1
                return None

            entry = self._cache[key]
            if entry['expires_at'] < time.time():
                del self._cache[key]
                if key in self._access_order:
                    del self._access_order[key]
                self._misses += 1
                self.logger.debug(f"Cache miss (expired): {key}")
                return None

            # Update access time for LRU
            self._access_order[key] = time.time()
            self._hits += 1
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
            # Check if we need to evict entries
            if self.max_size > 0 and key not in self._cache and len(self._cache) >= self.max_size:
                self._evict_lru()

            self._cache[key] = {
                'value': value,
                'expires_at': expires_at,
                'created_at': time.time()
            }
            self._access_order[key] = time.time()
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
                if key in self._access_order:
                    del self._access_order[key]
                self.logger.debug(f"Cache delete: {key}")
                return True
            return False

    def clear(self) -> None:
        """Clear all cache entries"""
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            self._access_order.clear()
            self._hits = 0
            self._misses = 0
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
                if key in self._access_order:
                    del self._access_order[key]

        if expired_keys:
            self.logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")

        return len(expired_keys)

    def _evict_lru(self) -> None:
        """Evict least recently used entry (must be called with lock held)"""
        if not self._access_order:
            # Fallback: remove oldest entry by creation time
            if self._cache:
                oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k]['created_at'])
                del self._cache[oldest_key]
                self.logger.debug(f"Evicted entry (by age): {oldest_key}")
            return

        # Find least recently accessed entry
        lru_key = min(self._access_order.keys(), key=lambda k: self._access_order[k])
        del self._cache[lru_key]
        del self._access_order[lru_key]
        self.logger.debug(f"Evicted LRU entry: {lru_key}")

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics

        Returns:
            Dictionary with cache statistics
        """
        with self._lock:
            total_requests = self._hits + self._misses
            hit_rate = (self._hits / total_requests * 100) if total_requests > 0 else 0
            return {
                'size': len(self._cache),
                'max_size': self.max_size,
                'hits': self._hits,
                'misses': self._misses,
                'hit_rate': f"{hit_rate:.2f}%",
                'default_ttl': self.default_ttl
            }

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
_cache_lock = Lock()


def get_cache(default_ttl: int = 300) -> Cache:
    """Get or create default cache instance (thread-safe)

    Args:
        default_ttl: Default time-to-live in seconds

    Returns:
        Cache instance
    """
    global _default_cache
    if _default_cache is None:
        with _cache_lock:
            # Double-check locking pattern
            if _default_cache is None:
                _default_cache = Cache(default_ttl)
    return _default_cache
