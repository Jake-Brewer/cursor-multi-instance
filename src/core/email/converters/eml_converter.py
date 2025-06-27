"""
EML format converter implementation.

This module provides functionality to convert email data to the EML format,
which is a standard format for storing individual email messages.
"""

import os
from email.message import EmailMessage
from typing import Any, Dict

from src.core.email.converter import BaseEmailConverter, ConversionError, EmailFormat


@BaseEmailConverter.register
class EmlConverter(BaseEmailConverter):
    """Converter for the EML email format."""

    @property
    def format(self) -> EmailFormat:
        """The format this converter handles."""
        return EmailFormat.EML

    def convert(self, email_data: Dict[str, Any], output_path: str) -> str:
        """
        Convert email data to EML format.

        Args:
            email_data: The email data to convert.
            output_path: Directory where the converted file should be saved.

        Returns:
            The path to the converted file.

        Raises:
            ConversionError: If the conversion fails.
        """
        try:
            # Create an EmailMessage object
            msg = EmailMessage()

            # Set headers
            msg["Subject"] = email_data.get("subject", "")
            msg["From"] = email_data.get("from", "")
            msg["To"] = email_data.get("to", "")
            msg["Date"] = email_data.get("date", "")

            # Set content
            if "html_content" in email_data:
                msg.set_content(email_data["html_content"], subtype="html")
            elif "text_content" in email_data:
                msg.set_content(email_data["text_content"])
            else:
                msg.set_content("No content available")

            # Add attachments if present
            if "attachments" in email_data and isinstance(
                email_data["attachments"], list
            ):
                for attachment in email_data["attachments"]:
                    if not isinstance(attachment, dict):
                        continue

                    content = attachment.get("content")
                    filename = attachment.get("filename", "attachment")
                    content_type = attachment.get(
                        "content_type", "application/octet-stream"
                    )

                    if content:
                        maintype, subtype = (
                            content_type.split("/", 1)
                            if "/" in content_type
                            else (content_type, "")
                        )
                        msg.add_attachment(
                            content,
                            maintype=maintype,
                            subtype=subtype,
                            filename=filename,
                        )

            # Generate filename
            filename = self.generate_filename(email_data, "eml")
            file_path = os.path.join(output_path, filename)

            # Ensure output directory exists
            os.makedirs(output_path, exist_ok=True)

            # Write to file
            with open(file_path, "wb") as f:
                f.write(msg.as_bytes())

            return file_path

        except Exception as e:
            raise ConversionError(f"Failed to convert email to EML format: {str(e)}")
