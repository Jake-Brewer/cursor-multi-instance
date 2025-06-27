"""
Email format manager module.

This module provides a high-level API for converting emails to different formats.
It handles the selection of appropriate converters and manages the conversion process.
"""

import os
from typing import Any, Dict, List, Optional, Union

from src.core.config import config_manager
from src.core.email.converter import BaseEmailConverter, ConversionError, EmailFormat


class EmailFormatManager:
    """
    Manager for email format conversion operations.

    This class provides a high-level API for converting emails to different formats.
    It handles the selection of appropriate converters and manages the conversion process.
    """

    def __init__(self):
        """Initialize the email format manager."""
        self.config = config_manager

    def get_default_format(self) -> EmailFormat:
        """
        Get the default email format from configuration.

        Returns:
            The default EmailFormat.
        """
        return BaseEmailConverter.get_default_format()

    def convert_email(
        self,
        email_data: Dict[str, Any],
        output_path: str,
        format_type: Optional[Union[EmailFormat, str]] = None,
    ) -> str:
        """
        Convert an email to the specified format.

        Args:
            email_data: The email data to convert.
            output_path: Directory where the converted file should be saved.
            format_type: The format to convert to. If None, uses the default format.

        Returns:
            The path to the converted file.

        Raises:
            ConversionError: If the conversion fails.
            ValueError: If the format is not supported.
        """
        # Determine format
        if format_type is None:
            format_type = self.get_default_format()
        elif isinstance(format_type, str):
            format_type = EmailFormat.from_string(format_type)

        # Get converter
        converter = BaseEmailConverter.get_converter(format_type)

        # Convert
        return converter.convert(email_data, output_path)

    def convert_email_to_all_formats(
        self, email_data: Dict[str, Any], output_path: str
    ) -> Dict[EmailFormat, str]:
        """
        Convert an email to all supported formats.

        Args:
            email_data: The email data to convert.
            output_path: Directory where the converted files should be saved.

        Returns:
            A dictionary mapping formats to file paths.

        Raises:
            ConversionError: If any conversion fails.
        """
        results = {}
        errors = []

        # Try each format
        for format_type in EmailFormat:
            try:
                file_path = self.convert_email(email_data, output_path, format_type)
                results[format_type] = file_path
            except Exception as e:
                errors.append(f"{format_type.name}: {str(e)}")

        # If all conversions failed, raise an error
        if not results and errors:
            raise ConversionError(f"All conversions failed: {'; '.join(errors)}")

        return results

    def get_supported_formats(self) -> List[str]:
        """
        Get a list of supported email formats.

        Returns:
            A list of format names.
        """
        return [format_type.name for format_type in EmailFormat]


# Singleton instance for easy access
email_format_manager = EmailFormatManager()
