"""
Helper utility functions
"""

import hashlib
import time
from datetime import datetime
from typing import Any, Callable, List, Optional


def get_timestamp() -> str:
    """Get current timestamp as formatted string

    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def calculate_hash(data: str, algorithm: str = "sha256") -> str:
    """Calculate hash of data

    Args:
        data: Input data to hash
        algorithm: Hash algorithm (sha256, md5, sha1)

    Returns:
        Hexadecimal hash string
    """
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(data.encode('utf-8'))
    return hash_obj.hexdigest()


def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator to retry function execution on failure

    Args:
        max_attempts: Maximum number of retry attempts
        delay: Delay between retries in seconds

    Returns:
        Decorated function
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(delay)
            # This should never be reached, but raise the last exception if it does
            if last_exception:
                raise last_exception
            raise RuntimeError("Retry decorator failed without exception")
        return wrapper
    return decorator


def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks

    Args:
        items: List to split
        chunk_size: Size of each chunk

    Returns:
        List of chunks
    """
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters

    Args:
        filename: Input filename

    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def format_size(size_bytes: int) -> str:
    """Format byte size to human readable format

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"
