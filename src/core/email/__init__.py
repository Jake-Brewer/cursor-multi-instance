"""
Email format conversion module for the Data Ingestor project.

This module provides functionality for converting emails to different formats:
- EML (standard email format)
- MBOX (for compatibility with email clients)
- PDF (for long-term archiving)
- HTML (for easy viewing)

Design decisions:
1. Modular approach with separate converters for each format
2. Common interface for all converters
3. Configuration-driven default format selection
4. Consistent naming scheme across all formats
5. Robust error handling for conversion failures
"""

from src.core.email.converter import BaseEmailConverter, ConversionError, EmailFormat
from src.core.email.manager import EmailFormatManager, email_format_manager

__all__ = [
    "BaseEmailConverter",
    "ConversionError",
    "EmailFormat",
    "EmailFormatManager",
    "email_format_manager",
]
