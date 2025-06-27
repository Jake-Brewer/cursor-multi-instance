"""
Email format converter module providing base classes and interfaces.

This module defines the base converter class and interfaces for converting
emails to different formats. It provides a common interface for all converters
and handles the registration of different converter implementations.
"""

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Dict, Type

from src.core.config import config_manager


class EmailFormat(Enum):
    """Supported email export formats."""

    EML = auto()
    MBOX = auto()
    PDF = auto()
    HTML = auto()

    @classmethod
    def from_string(cls, format_str: str) -> "EmailFormat":
        """Convert a string to an EmailFormat enum value."""
        try:
            return cls[format_str.upper()]
        except KeyError:
            formats = ", ".join([f.name for f in cls])
            raise ValueError(
                f"Unsupported format: {format_str}. " f"Supported formats: {formats}"
            )


class ConversionError(Exception):
    """Exception raised when email conversion fails."""

    pass


class BaseEmailConverter(ABC):
    """Base class for all email format converters."""

    # Registry of converter implementations
    _converters: Dict[EmailFormat, Type["BaseEmailConverter"]] = {}

    def __init__(self):
        """Initialize the converter with configuration."""
        self.config = config_manager

    @property
    @abstractmethod
    def format(self) -> EmailFormat:
        """The format this converter handles."""
        pass

    @abstractmethod
    def convert(self, email_data: Dict[str, Any], output_path: str) -> str:
        """
        Convert email data to the target format.

        Args:
            email_data: The email data to convert.
            output_path: Directory where the converted file should be saved.

        Returns:
            The path to the converted file.

        Raises:
            ConversionError: If the conversion fails.
        """
        pass

    @classmethod
    def register(
        cls, converter_class: Type["BaseEmailConverter"]
    ) -> Type["BaseEmailConverter"]:
        """
        Register a converter implementation.

        This is designed to be used as a decorator:

        @BaseEmailConverter.register
        class EmlConverter(BaseEmailConverter):
            ...

        Args:
            converter_class: The converter class to register.

        Returns:
            The registered converter class.
        """
        instance = converter_class()
        cls._converters[instance.format] = converter_class
        return converter_class

    @classmethod
    def get_converter(cls, format_type: EmailFormat) -> "BaseEmailConverter":
        """
        Get a converter instance for the specified format.

        Args:
            format_type: The email format to convert to.

        Returns:
            An instance of the appropriate converter.

        Raises:
            ValueError: If no converter is registered for the format.
        """
        if format_type not in cls._converters:
            raise ValueError(f"No converter registered for format: {format_type.name}")

        return cls._converters[format_type]()

    @classmethod
    def get_default_format(cls) -> EmailFormat:
        """
        Get the default email format from configuration.

        Returns:
            The default EmailFormat.
        """
        default_format = config_manager.get("email.default_format", "EML")
        return EmailFormat.from_string(default_format)

    @staticmethod
    def generate_filename(email_data: Dict[str, Any], format_name: str) -> str:
        """
        Generate a consistent filename for the converted email.

        Args:
            email_data: The email data.
            format_name: The format extension (e.g., 'eml', 'pdf').

        Returns:
            A filename string.
        """
        # Extract relevant fields for the filename
        subject = email_data.get("subject", "no_subject")
        date = email_data.get("date", "no_date")
        sender = email_data.get("from", "no_sender")

        # Clean up the fields for use in a filename
        subject = "".join(c if c.isalnum() or c in " -_" else "_" for c in subject)
        subject = subject[:50]  # Truncate long subjects

        # Format: YYYY-MM-DD_sender_subject.format
        if isinstance(date, str):
            date_str = date.split("T")[0] if "T" in date else date
        else:
            date_str = "no_date"

        # Clean up sender for filename
        if "@" in sender:
            sender = sender.split("@")[0]
        sender = "".join(c if c.isalnum() or c == "_" else "_" for c in sender)

        return f"{date_str}_{sender}_{subject}.{format_name.lower()}"
