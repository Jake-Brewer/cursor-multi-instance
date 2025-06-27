"""
HTML format converter implementation.

This module provides functionality to convert email data to HTML format,
which is useful for easy viewing in web browsers.
"""

import os
from typing import Any, Dict

from src.core.email.converter import (
    BaseEmailConverter,
    ConversionError,
    EmailFormat
)


@BaseEmailConverter.register
class HtmlConverter(BaseEmailConverter):
    """Converter for the HTML email format."""
    
    @property
    def format(self) -> EmailFormat:
        """The format this converter handles."""
        return EmailFormat.HTML
    
    def convert(self, email_data: Dict[str, Any], output_path: str) -> str:
        """
        Convert email data to HTML format.
        
        Args:
            email_data: The email data to convert.
            output_path: Directory where the converted file should be saved.
            
        Returns:
            The path to the converted file.
            
        Raises:
            ConversionError: If the conversion fails.
        """
        try:
            # Generate filename
            filename = self.generate_filename(email_data, 'html')
            file_path = os.path.join(output_path, filename)
            
            # Ensure output directory exists
            os.makedirs(output_path, exist_ok=True)
            
            # Extract email components
            subject = email_data.get('subject', 'No Subject')
            sender = email_data.get('from', 'Unknown Sender')
            recipient = email_data.get('to', 'Unknown Recipient')
            date = email_data.get('date', 'Unknown Date')
            
            # Use HTML content if available, otherwise use text content
            if 'html_content' in email_data:
                body = email_data['html_content']
            elif 'text_content' in email_data:
                # Convert plain text to HTML by replacing newlines with <br> tags
                body = email_data['text_content'].replace('\n', '<br>')
            else:
                body = 'No content available'
            
            # Generate attachments list if present
            attachments_html = ''
            if 'attachments' in email_data and isinstance(email_data['attachments'], list):
                attachments_html = '<h2>Attachments</h2><ul>'
                for attachment in email_data['attachments']:
                    if not isinstance(attachment, dict):
                        continue
                    
                    filename = attachment.get('filename', 'Unknown file')
                    attachments_html += f'<li>{filename}</li>'
                
                attachments_html += '</ul>'
            
            # Create HTML document
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{subject}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .email-container {{ max-width: 800px; margin: 0 auto; border: 1px solid #ddd; padding: 20px; }}
        .email-header {{ border-bottom: 1px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }}
        .email-body {{ line-height: 1.6; }}
        .email-attachments {{ margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="email-header">
            <h1>{subject}</h1>
            <p><strong>From:</strong> {sender}</p>
            <p><strong>To:</strong> {recipient}</p>
            <p><strong>Date:</strong> {date}</p>
        </div>
        <div class="email-body">
            {body}
        </div>
        <div class="email-attachments">
            {attachments_html}
        </div>
    </div>
</body>
</html>"""
            
            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            return file_path
            
        except Exception as e:
            raise ConversionError(
                f"Failed to convert email to HTML format: {str(e)}"
            ) 