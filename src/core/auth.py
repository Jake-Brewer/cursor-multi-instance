import os
from typing import Optional

from dotenv import load_dotenv


class AuthManager:
    """Manages loading and accessing authentication credentials."""

    _instance = None
    _credentials_loaded: bool = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AuthManager, cls).__new__(cls)
        return cls._instance

    def load_credentials(self, dotenv_path: Optional[str] = None) -> None:
        """
        Loads credentials from a .env file into environment variables.

        This method should be called once at the start of the application.

        Args:
            dotenv_path: Optional path to the .env file. If not provided,
                         python-dotenv will search for it automatically.
        """
        if self._credentials_loaded:
            return
        load_dotenv(dotenv_path=dotenv_path)
        self._credentials_loaded = True

    def get_credential(self, key: str) -> Optional[str]:
        """
        Retrieves a credential from the environment variables.

        Args:
            key: The name of the credential (environment variable) to retrieve.

        Returns:
            The credential value as a string, or None if not found.
        """
        return os.getenv(key)


# Singleton instance for easy access
auth_manager = AuthManager()
