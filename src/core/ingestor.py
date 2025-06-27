import importlib
import inspect
import pkgutil
from typing import Dict, Type

import src.providers
from src.providers.base import BaseProvider


class Ingestor:
    """Discovers and runs data providers."""

    def __init__(self):
        self.providers: Dict[str, Type[BaseProvider]] = self._discover_providers()

    def _discover_providers(self) -> Dict[str, Type[BaseProvider]]:
        """
        Dynamically discovers all BaseProvider subclasses in the providers module.

        Returns:
            A dictionary mapping provider names to provider classes.
        """
        provider_map = {}
        # The path must be set to the folder containing the provider modules
        for _, module_name, _ in pkgutil.iter_modules(src.providers.__path__):
            if module_name == "base":
                continue  # Skip the base class module

            module = importlib.import_module(f"src.providers.{module_name}")
            for _, member in inspect.getmembers(module, inspect.isclass):
                if issubclass(member, BaseProvider) and member is not BaseProvider:
                    # Instantiate to get the provider name
                    instance = member()
                    provider_map[instance.provider_name] = member
        return provider_map

    def list_providers(self) -> None:
        """Prints a list of available providers."""
        if not self.providers:
            print("No providers found.")
            return
        print("Available providers:")
        for name in self.providers.keys():
            print(f"- {name}")

    def run_provider(self, provider_name: str) -> None:
        """
        Runs a specific data provider.

        Args:
            provider_name: The name of the provider to run.
        """
        if provider_name not in self.providers:
            print(f"Error: Provider '{provider_name}' not found.")
            self.list_providers()
            return

        provider_class = self.providers[provider_name]
        provider_instance = provider_class()
        try:
            provider_instance.run()
        except Exception as e:
            # Basic error handling
            print(
                f"An error occurred while running provider " f"'{provider_name}': {e}"
            )
