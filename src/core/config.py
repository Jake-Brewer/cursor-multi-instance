import os
from typing import Any, Optional

import yaml


class ConfigError(Exception):
    """Custom exception for configuration errors."""

    pass


class ConfigManager:
    """Manages loading and accessing configuration from a YAML file."""

    _instance = None
    _config_data: Optional[dict] = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def load_config(self, config_path: str = "config.yaml") -> None:
        """
        Loads the configuration from a YAML file.

        The method looks for the file in the project root. It only loads
        the configuration once.

        Args:
            config_path: The path to the configuration file, relative to the
                         project root.

        Raises:
            ConfigError: If the config file is not found or cannot be parsed.
        """
        if self._config_data is not None:
            return

        try:
            # Assume the script is run from the project root
            full_path = os.path.join(os.getcwd(), config_path)
            if not os.path.exists(full_path):
                raise ConfigError(f"Configuration file not found at: {full_path}")

            with open(full_path, "r") as f:
                self._config_data = yaml.safe_load(f)

            if not isinstance(self._config_data, dict):
                self._config_data = {}
                raise ConfigError("Configuration file is not a valid YAML dictionary.")

        except (yaml.YAMLError, IOError) as e:
            raise ConfigError(f"Error loading configuration file: {e}") from e

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Retrieves a configuration value for a given key.

        Args:
            key: The configuration key to retrieve.
            default: The default value to return if the key is not found.

        Returns:
            The configuration value, or the default if not found.

        Raises:
            ConfigError: If config has not been loaded. Call load_config().
        """
        if self._config_data is None:
            raise ConfigError(
                "Configuration has not been loaded. Call load_config() first."
            )

        return self._config_data.get(key, default)


# Singleton instance for easy access
config_manager = ConfigManager()
