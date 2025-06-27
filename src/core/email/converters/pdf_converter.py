"""
PDF format converter implementation.

This module provides functionality to convert email data to PDF format,
which is useful for long-term archiving and printing.
"""

import os
import tempfile
from typing import Any, Dict

from fpdf import FPDF
from weasyprint import HTML

from src.core.email.converter import (
    BaseEmailConverter,
    ConversionError,
    EmailFormat
)
from src.core.email.converters.html_converter import HtmlConverter


@BaseEmailConverter.register
class PdfConverter(BaseEmailConverter):
    """Converter for the PDF email format."""
    
    @property
    def format(self) -> EmailFormat:
        """The format this converter handles."""
        return EmailFormat.PDF
    
    def convert(self, email_data: Dict[str, Any], output_path: str) -> str:
        """
        Convert email data to PDF format.
        
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
            filename = self.generate_filename(email_data, 'pdf')
            file_path = os.path.join(output_path, filename)
            
            # Ensure output directory exists
            os.makedirs(output_path, exist_ok=True)
            
            # Method selection based on available data
            if 'html_content' in email_data:
                # If we have HTML content, use WeasyPrint for better rendering
                self._convert_with_weasyprint(email_data, file_path)
            else:
                # Otherwise use FPDF for simpler text-based emails
                self._convert_with_fpdf(email_data, file_path)
                
            return file_path
            
        except Exception as e:
            raise ConversionError(
                f"Failed to convert email to PDF format: {str(e)}"
            )
    
    def _convert_with_weasyprint(
        self, email_data: Dict[str, Any], output_path: str
    ) -> None:
        """
        Convert email to PDF using WeasyPrint (better HTML rendering).
        
        Args:
            email_data: The email data to convert.
            output_path: Path where the PDF file should be saved.
        """
        # First convert to HTML
        html_converter = HtmlConverter()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate HTML file in temp directory
            html_path = html_converter.convert(email_data, temp_dir)
            
            # Convert HTML to PDF
            HTML(html_path).write_pdf(output_path)
    
    def _convert_with_fpdf(
        self, email_data: Dict[str, Any], output_path: str
    ) -> None:
        """
        Convert email to PDF using FPDF (simpler text-based approach).
        
        Args:
            email_data: The email data to convert.
            output_path: Path where the PDF file should be saved.
        """
        # Extract email components
        subject = email_data.get('subject', 'No Subject')
        sender = email_data.get('from', 'Unknown Sender')
        recipient = email_data.get('to', 'Unknown Recipient')
        date = email_data.get('date', 'Unknown Date')
        
        # Get content
        content = email_data.get('text_content', 'No content available')
        
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Set font
        pdf.set_font('Arial', 'B', 16)
        
        # Add title
        pdf.cell(0, 10, subject, 0, 1, 'C')
        pdf.ln(10)
        
        # Add metadata
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, f'From: {sender}', 0, 1)
        pdf.cell(0, 10, f'To: {recipient}', 0, 1)
        pdf.cell(0, 10, f'Date: {date}', 0, 1)
        pdf.ln(10)
        
        # Add content
        pdf.set_font('Arial', '', 12)
        
        # Split content into lines to avoid text overflow
        lines = content.split('\n')
        for line in lines:
            # Handle long lines by wrapping
            if len(line) > 80:  # Approximate character limit per line
                chunks = [line[i:i+80] for i in range(0, len(line), 80)]
                for chunk in chunks:
                    pdf.cell(0, 10, chunk, 0, 1)
            else:
                pdf.cell(0, 10, line, 0, 1)
        
        # Add attachments info if present
        if 'attachments' in email_data and isinstance(email_data['attachments'], list):
            pdf.ln(10)
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Attachments:', 0, 1)
            pdf.set_font('Arial', '', 12)
            
            for attachment in email_data['attachments']:
                if not isinstance(attachment, dict):
                    continue
                    
                filename = attachment.get('filename', 'Unknown file')
                pdf.cell(0, 10, f'- {filename}', 0, 1)
        
        # Output PDF
        pdf.output(output_path) 