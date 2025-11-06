"""
Configuration management module
"""

import json
import os
from typing import Any, Dict, Optional


class Config:
    """Configuration manager for GRUB application"""

    DEFAULT_CONFIG = {
        "app_name": "GRUB",
        "version": "1.0.0",
        "debug": False,
        "log_level": "INFO",
        "max_workers": 4,
    }

    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration

        Args:
            config_file: Path to configuration file
        """
        self._config: Dict[str, Any] = self.DEFAULT_CONFIG.copy()
        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value

        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value

    def load_from_file(self, filepath: str) -> None:
        """Load configuration from JSON file

        Args:
            filepath: Path to configuration file
        """
        with open(filepath, 'r') as f:
            loaded_config = json.load(f)
            self._config.update(loaded_config)

    def save_to_file(self, filepath: str) -> None:
        """Save configuration to JSON file

        Args:
            filepath: Path to save configuration
        """
        with open(filepath, 'w') as f:
            json.dump(self._config, f, indent=2)

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values

        Returns:
            Dictionary of all configuration values
        """
        return self._config.copy()
