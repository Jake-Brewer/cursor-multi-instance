# Email Format Conversion Design

## Overview

This document outlines the design for the email format conversion module in the Data Ingestor project. The module provides functionality to convert emails to different formats for archiving, viewing, and compatibility purposes.

## Supported Formats

The module supports the following email formats:

1. **EML** - Standard email format for individual messages
2. **MBOX** - Mailbox format for compatibility with email clients
3. **PDF** - Portable Document Format for long-term archiving and printing
4. **HTML** - Web format for easy viewing in browsers

## Architecture

### Class Diagram

```
┌─────────────────┐     ┌───────────────────┐
│ EmailFormat     │     │ EmailFormatManager │
│ (Enum)          │     │                   │
└─────────────────┘     └───────────┬───────┘
                                   │
                                   │ uses
                                   ▼
┌─────────────────┐     ┌───────────────────┐
│ ConversionError │     │ BaseEmailConverter │◄───────┐
│ (Exception)     │     │ (ABC)             │        │
└─────────────────┘     └───────────────────┘        │
                                 ▲                   │
                                 │                   │
                 ┌───────────────┴───────────────┐   │ registers
                 │               │               │   │
        ┌────────┴───────┐ ┌────┴─────────┐ ┌───┴───┴────────┐
        │ EmlConverter   │ │ MboxConverter│ │ PdfConverter   │
        └────────────────┘ └──────────────┘ └────────────────┘
                                              │
                                              │ uses
                                              ▼
                                     ┌────────────────────┐
                                     │ HtmlConverter      │
                                     └────────────────────┘
```

### Components

1. **EmailFormat (Enum)**: Defines the supported email formats.
2. **ConversionError (Exception)**: Custom exception for conversion failures.
3. **BaseEmailConverter (ABC)**: Abstract base class defining the interface for all converters.
4. **Format-specific Converters**: Implementations for each supported format.
5. **EmailFormatManager**: High-level API for email conversion operations.

## Design Decisions

1. **Modular Approach**: Each format has its own converter implementation, making it easy to add new formats.
2. **Common Interface**: All converters implement the same interface, allowing for consistent usage.
3. **Configuration-Driven**: Default format selection is driven by configuration settings.
4. **Consistent Naming**: Files are named consistently across formats using a standardized naming scheme.
5. **Robust Error Handling**: Comprehensive error handling with detailed error messages.
6. **Format-Specific Optimizations**:
   - HTML converter provides styled output for better readability
   - PDF converter uses different rendering engines based on content type
   - EML converter preserves all email metadata
   - MBOX converter follows standard mailbox format specifications

## Usage Examples

### Basic Usage

```python
from src.core.email import email_format_manager, EmailFormat

# Convert an email to the default format
file_path = email_format_manager.convert_email(email_data, output_directory)

# Convert to a specific format
pdf_path = email_format_manager.convert_email(
    email_data, 
    output_directory, 
    EmailFormat.PDF
)

# Convert to all supported formats
results = email_format_manager.convert_email_to_all_formats(
    email_data, 
    output_directory
)
```

### Configuration

The default format can be set in the application configuration:

```yaml
email:
  default_format: PDF  # Options: EML, MBOX, PDF, HTML
  output_directory: "./output/emails"
  naming_scheme: "{date}_{subject}_{sender}"
```

## Implementation Notes

1. **Dependencies**:
   - `fpdf2` for PDF generation
   - `weasyprint` for HTML-to-PDF conversion
   - Standard library modules for EML and MBOX formats

2. **Performance Considerations**:
   - PDF conversion is more resource-intensive, especially for large emails
   - HTML conversion preserves formatting but may not be suitable for all email types
   - EML is the most efficient format for storage and future processing

3. **Security**:
   - All converters sanitize inputs to prevent injection attacks
   - External content references in HTML emails are not automatically loaded

## Future Enhancements

1. Add support for MSG format (Microsoft Outlook)
2. Implement batch conversion for multiple emails
3. Add preview generation for quick viewing
4. Support for embedded images in PDF and HTML formats
5. Compression options for large attachments
