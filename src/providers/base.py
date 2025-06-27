from abc import ABC, abstractmethod
from typing import Any

from src.core.auth import auth_manager
from src.core.config import config_manager
from src.core.data_handler import DataHandler


class BaseProvider(ABC):
    """Abstract base class for all data providers."""

    def __init__(self):
        self.auth = auth_manager
        self.config = config_manager
        self.data_handler = DataHandler()
        self.auth.load_credentials()
        self.config.load_config()

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """The unique name of the provider (e.g., 'google', 'twitter')."""
        raise NotImplementedError

    @abstractmethod
    def authenticate(self) -> None:
        """
        Handles authentication with the provider.

        This method should use the AuthManager to get credentials and
        establish a session or get an API client.
        """
        raise NotImplementedError

    @abstractmethod
    def fetch_data(self) -> Any:
        """
        Fetches the data from the provider.

        Returns:
            The raw data fetched from the provider.
        """
        raise NotImplementedError

    def run(self) -> None:
        """
        Executes the full data ingestion process for the provider.
        """
        print(f"Running provider: {self.provider_name}")
        self.authenticate()
        print("Authentication successful.")
        data = self.fetch_data()
        print("Data fetched successfully.")
        file_path = self.data_handler.save_data(data, self.provider_name)
        print(f"Data saved to: {file_path}")
