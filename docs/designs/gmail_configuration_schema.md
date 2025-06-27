# Gmail Configuration Schema Design

## Overview

This document outlines the design for the Gmail provider configuration schema in the Data Ingestor project. The configuration schema will define all available options for the Gmail provider, including API rate limits, authentication settings, data filtering options, and output format preferences.

## Configuration Structure

The Gmail provider configuration will be added to the existing `config.yaml` file under a dedicated `gmail` section. The schema will follow a hierarchical structure for better organization and readability.

```yaml
providers:
  gmail:
    # Gmail-specific configuration options
    auth:
      # Authentication settings
    rate_limiting:
      # Rate limiting settings
    data:
      # Data selection and filtering
    output:
      # Output format and storage options
```

## Configuration Options

### Authentication Settings

```yaml
providers:
  gmail:
    auth:
      credentials_file: "~/.data-ingestor/gmail_credentials.json"  # Path to OAuth credentials file
      token_file: "~/.data-ingestor/gmail_token.json"  # Path to store OAuth tokens
      scopes:                                          # OAuth scopes to request
        - "https://www.googleapis.com/auth/gmail.readonly"
      browser_open: true                               # Whether to open browser for OAuth flow
      local_server:
        port: 8080                                     # Port for OAuth callback server
        timeout: 300                                   # Timeout in seconds for OAuth callback
```

### Rate Limiting Settings

```yaml
providers:
  gmail:
    rate_limiting:
      requests_per_day: 1000000                        # Maximum requests per day (Gmail limit)
      requests_per_second: 5                           # Maximum requests per second
      requests_per_user_per_second: 2                  # Maximum requests per user per second
      max_batch_size: 100                              # Maximum batch size for batch requests
      backoff:
        initial_delay: 1                               # Initial delay in seconds for retries
        max_delay: 60                                  # Maximum delay in seconds for retries
        factor: 2                                      # Exponential backoff factor
        jitter: 0.1                                    # Random jitter factor (0.0-1.0)
      quota_exceeded_behavior: "wait"                  # Options: "wait", "abort", "notify"
      logging:
        enabled: true                                  # Enable rate limit logging
        level: "info"                                  # Log level for rate limit events
```

### Data Selection and Filtering

```yaml
providers:
  gmail:
    data:
      labels:
        include:                                       # Labels to include (empty = all)
          - "INBOX"
          - "SENT"
        exclude:                                       # Labels to exclude
          - "TRASH"
          - "SPAM"
        system_labels: true                            # Include Gmail system labels
      date_range:
        start: "2023-01-01"                            # Start date for email retrieval (ISO format)
        end: "now"                                     # End date for email retrieval (ISO format or "now")
      filters:
        max_emails: 1000                               # Maximum number of emails to retrieve (0 = no limit)
        has_attachment: null                           # Filter by attachment presence (true/false/null)
        size_larger_than: 0                            # Size in bytes (0 = no filter)
        size_smaller_than: 0                           # Size in bytes (0 = no filter)
        include_drafts: false                          # Include draft emails
      search:
        default_operator: "AND"                        # Default operator for search terms
        saved_searches: {}                             # Named saved searches
```

### Output Format and Storage Options

```yaml
providers:
  gmail:
    output:
      format:
        default: "eml"                                 # Default format (eml, mbox, pdf, html)
        available:                                     # Available formats
          - "eml"
          - "mbox"
          - "pdf"
          - "html"
      naming:
        pattern: "{date}_{subject}_{id}"               # Naming pattern for email files
        sanitize_filenames: true                       # Sanitize filenames for filesystem compatibility
        max_filename_length: 255                       # Maximum filename length
      attachments:
        save: true                                     # Save email attachments
        location: "with_email"                         # Options: "with_email", "separate_folder"
        folder_name: "attachments"                     # Folder name for attachments if separate
      metadata:
        save: true                                     # Save email metadata
        format: "json"                                 # Format for metadata (json, yaml)
      structure:
        preserve_labels: true                          # Preserve Gmail label structure in folders
        handling_multiple_labels: "link"               # Options: "link", "copy", "primary_only"
```

## Validation Rules

The configuration schema will include the following validation rules:

1. **Type Checking**: All values must match their expected types (string, number, boolean, etc.)
2. **Range Validation**: Numeric values must be within acceptable ranges
3. **Format Validation**: Dates must be in ISO format or the special value "now"
4. **Enum Validation**: Values for fields like `quota_exceeded_behavior` must be one of the predefined options
5. **Path Validation**: File paths must be valid and accessible
6. **Dependency Validation**: Some options may depend on others (e.g., attachment location depends on attachment saving being enabled)

## Default Configuration

A default configuration will be provided in `config.yaml.example` with reasonable defaults for all options. This will serve as both documentation and a starting point for users.

## Implementation Details

### Configuration Loading

1. The configuration will be loaded by the `ConfigManager` class in `src/core/config.py`
2. Gmail-specific configuration validation will be implemented in `src/providers/gmail.py`
3. The provider will access its configuration through a standard interface provided by the `ConfigManager`

### Schema Validation

The schema validation will use the following approach:

1. Define a schema using a library like `pydantic` or `jsonschema`
2. Validate the loaded configuration against this schema
3. Provide clear error messages for validation failures
4. Apply default values for missing options

## Usage Examples

### Basic Configuration

```yaml
providers:
  gmail:
    auth:
      credentials_file: "~/.data-ingestor/gmail_credentials.json"
    data:
      labels:
        include:
          - "INBOX"
    output:
      format:
        default: "eml"
```

### Advanced Configuration

```yaml
providers:
  gmail:
    auth:
      credentials_file: "~/.data-ingestor/gmail_credentials.json"
      token_file: "~/.data-ingestor/gmail_token.json"
      scopes:
        - "https://www.googleapis.com/auth/gmail.readonly"
    rate_limiting:
      requests_per_second: 2
      backoff:
        initial_delay: 2
        max_delay: 120
    data:
      labels:
        include:
          - "INBOX"
          - "SENT"
        exclude:
          - "SPAM"
      date_range:
        start: "2023-01-01"
        end: "2023-12-31"
      filters:
        has_attachment: true
        size_larger_than: 1048576  # 1MB
    output:
      format:
        default: "pdf"
      attachments:
        location: "separate_folder"
      structure:
        preserve_labels: true
```

## Testing Strategy

The configuration schema will be tested with the following test cases:

1. **Valid Configuration**: Test that valid configurations are accepted
2. **Invalid Types**: Test that invalid types are rejected with clear error messages
3. **Invalid Values**: Test that values outside acceptable ranges are rejected
4. **Missing Required Fields**: Test that missing required fields are detected
5. **Default Values**: Test that default values are correctly applied
6. **Dependency Rules**: Test that dependent configuration options are correctly validated

## Future Considerations

1. **Configuration UI**: A future enhancement could include a web-based UI for configuring the Gmail provider
2. **Configuration Presets**: Predefined configuration presets for common use cases
3. **Dynamic Validation**: Runtime validation of configuration options based on Gmail API capabilities
4. **Configuration Migration**: Tools for migrating from older configuration formats
