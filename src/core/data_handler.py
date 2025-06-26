# <!-- LOCKED:DIA:2023-05-28T15:20:00Z:2023-05-28T15:25:00Z -->
import datetime
import json
import os
from typing import Any, Dict, List, Union

from .config import config_manager


class DataHandler:
    """Handles saving data to the filesystem in a structured way."""

    def __init__(self):
        config_manager.load_config()
        self.base_output_dir = config_manager.get("output_directory", "output")

    def save_data(
        self,
        data: Union[Dict[str, Any], List[Any]],
        provider_name: str,
        filename: str = "data.json",
    ) -> str:
        """
        Saves data to a timestamped folder for a specific provider.

        The directory structure will be:
        <base_output_dir>/<provider_name>/<YYYY-MM-DD_HH-MM-SS>/<filename>

        Args:
            data: The data to save (a dictionary or list).
            provider_name: The name of the provider (e.g., 'google').
            filename: The name of the file to save the data in.

        Returns:
            The full path to the saved file.

        Raises:
            IOError: If the data cannot be written to the file.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        dir_parts = [self.base_output_dir, provider_name, timestamp]
        output_path = os.path.join(*dir_parts)

        try:
            os.makedirs(output_path, exist_ok=True)
            file_path = os.path.join(output_path, filename)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            return file_path
        except (IOError, OSError) as e:
            # In a real app, we'd have a proper logger here
            print(f"Error saving data: {e}")
            raise IOError(f"Could not write to file {file_path}") from e
