# Data Ingestor

## Overview

This project provides a flexible data ingestion and processing system with support for multiple providers and dynamic tool registration.

## Server Entry Point

### Running the MCP Server

The main server entry point is located at `src/__main__.py`. You can run the server using Python:

```bash
python -m src
```

#### Command-Line Options

- `--host`: Specify the host to bind the server to (default: 0.0.0.0)
- `--port`: Specify the port to run the server on (default: 8000)

Example:

```bash
python -m src --host 127.0.0.1 --port 9000
```

### Server Features

- Dynamic tool discovery and registration
- CORS support for cross-origin requests
- Configurable host and port
- Automatic module scanning for tools

## Features

- Download your personal data from multiple platforms
- Modular and extensible for new data sources
- No scraping or automation that violates host TOS
- Focus on privacy, transparency, and user control

## Usage

1. Clone this repository.
2. Install dependencies (see below).
3. Run the provided scripts to download your data from supported sources.

> **Note:** This tool is intended for personal use only. Always review and comply with the Terms of Service of each data provider. This project does not support or condone any activity that would violate those terms.

## Installation

1. Clone the repository
2. Create a virtual environment
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

```bash
python -m pytest src/tests/
```

## License

This project is provided **without a license**. All rights reserved by the author. For personal use only.

## Contributing

Please read our contribution guidelines before submitting pull requests.

## Disclaimer

This project is not affiliated with or endorsed by any data provider. Use at your own risk.

## Linear Task Monitoring

### Overview

The `LinearTaskMonitor` provides a robust, adaptive monitoring system for Linear tasks with the following key features:

- **Adaptive Polling**: Dynamically adjusts polling intervals using exponential backoff
- **Error Resilience**: Configurable retry mechanism with maximum retry limits
- **Flexible Task Filtering**: Filter tasks by state and priority
- **Graceful Shutdown**: Handles interruption signals cleanly

### Configuration Options

```python
monitor = LinearTaskMonitor(
    linear_client=client,
    poll_interval=5,      # Base polling interval (seconds)
    max_retries=3,        # Maximum retry attempts
    backoff_factor=2.0    # Exponential backoff multiplier
)
```

### Usage Example

```python
# Monitor tasks in 'backlog' or 'in_progress' states
# with priority >= 2
monitor.start_monitoring(
    state_filter=['backlog', 'in_progress'],
    priority_threshold=2,
    timeout=3600  # Optional: Run for 1 hour
)
```

### Error Handling

- Automatically retries on connection errors
- Exponential backoff to prevent overwhelming the API
- Configurable maximum retry attempts
