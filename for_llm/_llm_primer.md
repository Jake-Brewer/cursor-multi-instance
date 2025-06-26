# Data Ingestor Project Primer
<!-- Updated: 2023-05-28T14:35:12Z -->

This document provides essential context for LLM agents working on the Data Ingestor project.

## Project Overview

Data Ingestor is a Python project designed to help individuals download and archive their personal information from various online sources while strictly adhering to each host's Terms of Service (TOS). The project emphasizes ethical data collection, privacy, and user control.

## Key Principles

1. **TOS Compliance**: All data collection must strictly adhere to the terms of service of each platform.
2. **Personal Use Only**: Tools are intended for individuals to access their own data, not for scraping or bulk collection.
3. **Privacy First**: User data security and privacy are paramount.
4. **Modularity**: Each data source should be implemented as a separate module for easy maintenance.

## Todo Management

Maintain a todo file named `for_llm_todo_<agent_name>.md` in the project root. This file should:

1. List all tasks in progress and planned
2. Include task status (TODO, IN_PROGRESS, BLOCKED, DONE)
3. Be updated in real-time as tasks are completed or new tasks are identified
4. Include brief notes on implementation details or blockers

## Development Guidelines

1. Follow PEP 8 style guidelines for Python code
2. Write comprehensive docstrings and comments
3. Include unit tests for all functionality
4. Maintain a clean, modular architecture
5. Use type hints to improve code readability and IDE support
6. Prefer standard library solutions when possible

## Repository Structure

- `src/` - Main source code
- `src/providers/` - Data provider-specific modules
- `src/core/` - Core functionality shared across providers
- `tests/` - Test suite
- `docs/` - Documentation
- `for_llm/` - Resources for LLM agents

Remember to register in the agent registry and follow file locking protocols before making changes.
