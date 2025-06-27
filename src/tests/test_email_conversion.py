"""
Tests for the email format conversion module.
"""

import os
import tempfile
from unittest import mock

import pytest

from src.core.email import EmailFormat, ConversionError, email_format_manager
from src.core.email.converter import BaseEmailConverter
from src.core.email.converters.eml_converter import EmlConverter
from src.core.email.converters.html_converter import HtmlConverter
from src.core.email.converters.mbox_converter import MboxConverter
from src.core.email.converters.pdf_converter import PdfConverter


# Sample email data for testing
@pytest.fixture
def sample_email_data():
    """Sample email data for testing."""
    return {
        "subject": "Test Email",
        "from": "sender@example.com",
        "to": "recipient@example.com",
        "date": "Mon, 1 Jan 2023 12:00:00 +0000",
        "text_content": "This is a test email content.",
        "html_content": "<html><body><p>This is a test email content.</p></body></html>",
        "attachments": [
            {
                "filename": "test.txt",
                "content": b"Test attachment content",
                "content_type": "text/plain",
            }
        ],
    }


class TestEmailFormat:
    """Tests for the EmailFormat enum."""

    def test_from_string_valid(self):
        """Test converting valid strings to EmailFormat."""
        assert EmailFormat.from_string("EML") == EmailFormat.EML
        assert EmailFormat.from_string("MBOX") == EmailFormat.MBOX
        assert EmailFormat.from_string("PDF") == EmailFormat.PDF
        assert EmailFormat.from_string("HTML") == EmailFormat.HTML

        # Case insensitive
        assert EmailFormat.from_string("eml") == EmailFormat.EML
        assert EmailFormat.from_string("mbox") == EmailFormat.MBOX

    def test_from_string_invalid(self):
        """Test converting invalid strings to EmailFormat."""
        with pytest.raises(ValueError):
            EmailFormat.from_string("INVALID")


class TestBaseEmailConverter:
    """Tests for the BaseEmailConverter class."""

    def test_register_decorator(self):
        """Test that converters are registered correctly."""
        converters = BaseEmailConverter.get_converters()

        # Check that all expected converters are registered
        assert any(isinstance(c, EmlConverter) for c in converters)
        assert any(isinstance(c, MboxConverter) for c in converters)
        assert any(isinstance(c, PdfConverter) for c in converters)
        assert any(isinstance(c, HtmlConverter) for c in converters)

    def test_get_converter(self):
        """Test getting a converter for a specific format."""
        eml_converter = BaseEmailConverter.get_converter(EmailFormat.EML)
        assert isinstance(eml_converter, EmlConverter)

        mbox_converter = BaseEmailConverter.get_converter(EmailFormat.MBOX)
        assert isinstance(mbox_converter, MboxConverter)

        pdf_converter = BaseEmailConverter.get_converter(EmailFormat.PDF)
        assert isinstance(pdf_converter, PdfConverter)

        html_converter = BaseEmailConverter.get_converter(EmailFormat.HTML)
        assert isinstance(html_converter, HtmlConverter)

    def test_get_default_format(self):
        """Test getting the default format."""
        # Mock the config to return a specific default format
        with mock.patch(
            "src.core.email.converter.config_manager.get", return_value="PDF"
        ):
            default_format = BaseEmailConverter.get_default_format()
            assert default_format == EmailFormat.PDF

    def test_generate_filename(self):
        """Test generating filenames."""
        converter = next(iter(BaseEmailConverter.get_converters()))
        email_data = {
            "subject": "Test Subject",
            "from": "sender@example.com",
            "date": "2023-01-01T12:00:00Z",
        }

        # Test with default naming scheme
        with mock.patch(
            "src.core.email.converter.config_manager.get",
            return_value="{date}_{subject}_{sender}",
        ):
            filename = converter.generate_filename(email_data, "eml")
            assert (
                "2023-01-01T12:00:00Z_Test_Subject_sender@example.com.eml" == filename
            )

        # Test with custom naming scheme
        with mock.patch(
            "src.core.email.converter.config_manager.get",
            return_value="{subject}-{sender}",
        ):
            filename = converter.generate_filename(email_data, "pdf")
            assert "Test_Subject-sender@example.com.pdf" == filename


class TestConverters:
    """Tests for the individual converters."""

    def test_eml_converter(self, sample_email_data):
        """Test the EML converter."""
        converter = EmlConverter()

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = converter.convert(sample_email_data, temp_dir)

            # Check that the file was created
            assert os.path.exists(file_path)
            assert file_path.endswith(".eml")

            # Check file content
            with open(file_path, "rb") as f:
                content = f.read()
                assert b"Subject: Test Email" in content
                assert b"From: sender@example.com" in content
                assert b"To: recipient@example.com" in content

    def test_mbox_converter(self, sample_email_data):
        """Test the MBOX converter."""
        converter = MboxConverter()

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = converter.convert(sample_email_data, temp_dir)

            # Check that the file was created
            assert os.path.exists(file_path)
            assert file_path.endswith(".mbox")

    def test_html_converter(self, sample_email_data):
        """Test the HTML converter."""
        converter = HtmlConverter()

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = converter.convert(sample_email_data, temp_dir)

            # Check that the file was created
            assert os.path.exists(file_path)
            assert file_path.endswith(".html")

            # Check file content
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                assert "Test Email" in content
                assert "sender@example.com" in content
                assert "recipient@example.com" in content

    @mock.patch("src.core.email.converters.pdf_converter.HTML")
    def test_pdf_converter_with_html(self, mock_html, sample_email_data):
        """Test the PDF converter with HTML content."""
        converter = PdfConverter()

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = converter.convert(sample_email_data, temp_dir)

            # Check that the file was created
            assert os.path.exists(file_path)
            assert file_path.endswith(".pdf")

            # Check that WeasyPrint was called
            mock_html.assert_called_once()

    @mock.patch("src.core.email.converters.pdf_converter.FPDF")
    def test_pdf_converter_with_text(self, mock_fpdf, sample_email_data):
        """Test the PDF converter with text content only."""
        # Remove HTML content to force using FPDF
        sample_email_data.pop("html_content")

        converter = PdfConverter()

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = converter.convert(sample_email_data, temp_dir)

            # Check that the file was created
            assert os.path.exists(file_path)
            assert file_path.endswith(".pdf")

            # Check that FPDF was called
            mock_fpdf.assert_called_once()


class TestEmailFormatManager:
    """Tests for the EmailFormatManager class."""

    def test_get_default_format(self):
        """Test getting the default format."""
        with mock.patch(
            "src.core.email.converter.BaseEmailConverter.get_default_format",
            return_value=EmailFormat.PDF,
        ):
            assert email_format_manager.get_default_format() == EmailFormat.PDF

    def test_convert_email_default_format(self, sample_email_data):
        """Test converting an email with the default format."""
        with mock.patch(
            "src.core.email.manager.BaseEmailConverter.get_default_format",
            return_value=EmailFormat.EML,
        ):
            with mock.patch(
                "src.core.email.manager.BaseEmailConverter.get_converter"
            ) as mock_get_converter:
                mock_converter = mock.MagicMock()
                mock_converter.convert.return_value = "/path/to/file.eml"
                mock_get_converter.return_value = mock_converter

                result = email_format_manager.convert_email(
                    sample_email_data, "/output"
                )

                assert result == "/path/to/file.eml"
                mock_get_converter.assert_called_once_with(EmailFormat.EML)
                mock_converter.convert.assert_called_once_with(
                    sample_email_data, "/output"
                )

    def test_convert_email_specific_format(self, sample_email_data):
        """Test converting an email with a specific format."""
        with mock.patch(
            "src.core.email.manager.BaseEmailConverter.get_converter"
        ) as mock_get_converter:
            mock_converter = mock.MagicMock()
            mock_converter.convert.return_value = "/path/to/file.pdf"
            mock_get_converter.return_value = mock_converter

            result = email_format_manager.convert_email(
                sample_email_data, "/output", EmailFormat.PDF
            )

            assert result == "/path/to/file.pdf"
            mock_get_converter.assert_called_once_with(EmailFormat.PDF)
            mock_converter.convert.assert_called_once_with(sample_email_data, "/output")

    def test_convert_email_string_format(self, sample_email_data):
        """Test converting an email with a format specified as a string."""
        with mock.patch(
            "src.core.email.manager.EmailFormat.from_string",
            return_value=EmailFormat.HTML,
        ) as mock_from_string:
            with mock.patch(
                "src.core.email.manager.BaseEmailConverter.get_converter"
            ) as mock_get_converter:
                mock_converter = mock.MagicMock()
                mock_converter.convert.return_value = "/path/to/file.html"
                mock_get_converter.return_value = mock_converter

                result = email_format_manager.convert_email(
                    sample_email_data, "/output", "HTML"
                )

                assert result == "/path/to/file.html"
                mock_from_string.assert_called_once_with("HTML")
                mock_get_converter.assert_called_once_with(EmailFormat.HTML)
                mock_converter.convert.assert_called_once_with(
                    sample_email_data, "/output"
                )

    def test_convert_email_to_all_formats(self, sample_email_data):
        """Test converting an email to all formats."""
        with mock.patch(
            "src.core.email.manager.EmailFormatManager.convert_email"
        ) as mock_convert:
            # Set up return values for each format
            mock_convert.side_effect = [
                "/path/to/file.eml",
                "/path/to/file.mbox",
                "/path/to/file.pdf",
                "/path/to/file.html",
            ]

            results = email_format_manager.convert_email_to_all_formats(
                sample_email_data, "/output"
            )

            assert len(results) == 4
            assert results[EmailFormat.EML] == "/path/to/file.eml"
            assert results[EmailFormat.MBOX] == "/path/to/file.mbox"
            assert results[EmailFormat.PDF] == "/path/to/file.pdf"
            assert results[EmailFormat.HTML] == "/path/to/file.html"

            assert mock_convert.call_count == 4

    def test_convert_email_to_all_formats_with_errors(self, sample_email_data):
        """Test converting an email to all formats with some errors."""
        with mock.patch(
            "src.core.email.manager.EmailFormatManager.convert_email"
        ) as mock_convert:
            # Set up return values and errors for each format
            mock_convert.side_effect = [
                "/path/to/file.eml",
                ConversionError("MBOX error"),
                "/path/to/file.pdf",
                ConversionError("HTML error"),
            ]

            results = email_format_manager.convert_email_to_all_formats(
                sample_email_data, "/output"
            )

            assert len(results) == 2
            assert results[EmailFormat.EML] == "/path/to/file.eml"
            assert results[EmailFormat.PDF] == "/path/to/file.pdf"
            assert EmailFormat.MBOX not in results
            assert EmailFormat.HTML not in results

            assert mock_convert.call_count == 4

    def test_convert_email_to_all_formats_all_fail(self, sample_email_data):
        """Test converting an email to all formats when all conversions fail."""
        with mock.patch(
            "src.core.email.manager.EmailFormatManager.convert_email"
        ) as mock_convert:
            # Set up errors for all formats
            mock_convert.side_effect = [
                ConversionError("EML error"),
                ConversionError("MBOX error"),
                ConversionError("PDF error"),
                ConversionError("HTML error"),
            ]

            with pytest.raises(ConversionError) as excinfo:
                email_format_manager.convert_email_to_all_formats(
                    sample_email_data, "/output"
                )

            assert "All conversions failed" in str(excinfo.value)
            assert mock_convert.call_count == 4

    def test_get_supported_formats(self):
        """Test getting the list of supported formats."""
        formats = email_format_manager.get_supported_formats()

        assert len(formats) == 4
        assert "EML" in formats
        assert "MBOX" in formats
        assert "PDF" in formats
        assert "HTML" in formats
