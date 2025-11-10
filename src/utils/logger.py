"""
Logging system for GRUB application
"""

import logging
import os
from datetime import datetime
from typing import Optional
from threading import Lock


class Logger:
    """Custom logger for GRUB application"""

    def __init__(self, name: str = "GRUB", level: str = "INFO", log_file: Optional[str] = None):
        """Initialize logger

        Args:
            name: Logger name
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional log file path
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))

        # Clear existing handlers
        self.logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, level.upper()))
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # File handler (if specified)
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(getattr(logging, level.upper()))
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message: str) -> None:
        """Log debug message"""
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """Log info message"""
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Log warning message"""
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Log error message"""
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """Log critical message"""
        self.logger.critical(message)

    def exception(self, message: str) -> None:
        """Log exception with traceback"""
        self.logger.exception(message)


# Global logger instance
_default_logger: Optional[Logger] = None
_logger_lock = Lock()


def get_logger(name: str = "GRUB", level: str = "INFO", log_file: Optional[str] = None) -> Logger:
    """Get or create logger instance (thread-safe)

    Args:
        name: Logger name
        level: Logging level
        log_file: Optional log file path

    Returns:
        Logger instance
    """
    global _default_logger
    if _default_logger is None:
        with _logger_lock:
            # Double-check locking pattern
            if _default_logger is None:
                _default_logger = Logger(name, level, log_file)
    return _default_logger
