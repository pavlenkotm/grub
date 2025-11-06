"""
Security utilities for encryption, hashing, and token generation
"""

import hashlib
import hmac
import secrets
import base64
from typing import Optional

from .logger import get_logger


class Security:
    """Security utilities for common cryptographic operations"""

    def __init__(self):
        """Initialize security utilities"""
        self.logger = get_logger()

    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Generate cryptographically secure random token

        Args:
            length: Length of token in bytes

        Returns:
            Hexadecimal token string
        """
        return secrets.token_hex(length)

    @staticmethod
    def generate_url_safe_token(length: int = 32) -> str:
        """Generate URL-safe random token

        Args:
            length: Length of token in bytes

        Returns:
            URL-safe token string
        """
        return secrets.token_urlsafe(length)

    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> tuple:
        """Hash password with salt

        Args:
            password: Password to hash
            salt: Optional salt (generated if not provided)

        Returns:
            Tuple of (hashed_password, salt)
        """
        if salt is None:
            salt = secrets.token_hex(16)

        # Use PBKDF2 for password hashing
        hash_obj = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # Number of iterations
        )
        hashed = base64.b64encode(hash_obj).decode('utf-8')
        return hashed, salt

    @staticmethod
    def verify_password(password: str, hashed_password: str, salt: str) -> bool:
        """Verify password against hash

        Args:
            password: Password to verify
            hashed_password: Stored password hash
            salt: Salt used for hashing

        Returns:
            True if password matches
        """
        new_hash, _ = Security.hash_password(password, salt)
        return hmac.compare_digest(new_hash, hashed_password)

    @staticmethod
    def hash_data(data: str, algorithm: str = 'sha256') -> str:
        """Hash data using specified algorithm

        Args:
            data: Data to hash
            algorithm: Hash algorithm (sha256, sha512, md5, etc.)

        Returns:
            Hexadecimal hash string
        """
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(data.encode('utf-8'))
        return hash_obj.hexdigest()

    @staticmethod
    def hmac_sign(message: str, key: str, algorithm: str = 'sha256') -> str:
        """Create HMAC signature

        Args:
            message: Message to sign
            key: Secret key
            algorithm: Hash algorithm

        Returns:
            Hexadecimal HMAC signature
        """
        return hmac.new(
            key.encode('utf-8'),
            message.encode('utf-8'),
            algorithm
        ).hexdigest()

    @staticmethod
    def hmac_verify(message: str, key: str, signature: str, algorithm: str = 'sha256') -> bool:
        """Verify HMAC signature

        Args:
            message: Message to verify
            key: Secret key
            signature: Signature to verify against
            algorithm: Hash algorithm

        Returns:
            True if signature is valid
        """
        expected = Security.hmac_sign(message, key, algorithm)
        return hmac.compare_digest(expected, signature)

    @staticmethod
    def encode_base64(data: str) -> str:
        """Encode data to base64

        Args:
            data: Data to encode

        Returns:
            Base64 encoded string
        """
        return base64.b64encode(data.encode('utf-8')).decode('utf-8')

    @staticmethod
    def decode_base64(encoded: str) -> str:
        """Decode base64 data

        Args:
            encoded: Base64 encoded string

        Returns:
            Decoded string
        """
        return base64.b64decode(encoded.encode('utf-8')).decode('utf-8')

    @staticmethod
    def constant_time_compare(a: str, b: str) -> bool:
        """Constant-time string comparison to prevent timing attacks

        Args:
            a: First string
            b: Second string

        Returns:
            True if strings are equal
        """
        return hmac.compare_digest(a, b)

    def generate_api_key(self, prefix: str = "grub") -> str:
        """Generate API key with prefix

        Args:
            prefix: Prefix for API key

        Returns:
            API key string
        """
        token = self.generate_token(32)
        api_key = f"{prefix}_{token}"
        self.logger.debug("Generated API key")
        return api_key

    @staticmethod
    def generate_random_bytes(length: int = 32) -> bytes:
        """Generate cryptographically secure random bytes

        Args:
            length: Number of bytes to generate

        Returns:
            Random bytes
        """
        return secrets.token_bytes(length)


# Global security instance
_security_instance: Optional[Security] = None


def get_security() -> Security:
    """Get or create security instance

    Returns:
        Security instance
    """
    global _security_instance
    if _security_instance is None:
        _security_instance = Security()
    return _security_instance
