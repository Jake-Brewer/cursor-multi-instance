# DataIngestorAgent Todo List
<!-- Updated: 2023-05-28T14:55:00Z -->

## Project Setup Tasks

### Repository Structure

- [x] Initialize git repository
- [x] Create .gitignore for Python and Markdown
- [x] Create README.md with project description
- [x] Create agent registry and primer files
- [x] Set up basic directory structure (src, tests, docs)
- [x] Create requirements.txt with basic dependencies

### Core Framework

- [ ] **Design core architecture and interfaces** `IN_PROGRESS`
  - [x] Create architecture design document
  - [x] Implement `ConfigManager`
  - [x] Implement `AuthManager`
  - [x] Implement `DataHandler`
  - [x] Implement `BaseProvider` ABC
  - [x] Implement `Ingestor` orchestrator
  - [x] Implement CLI

### Core Framework Testing

- [x] Implement `DummyProvider` to test framework
- [x] Verify provider discovery and execution via CLI

### Initial Providers

- [ ] **Research API requirements for initial supported platforms** `IN_PROGRESS`
  - [ ] Google Takeout: Research automation methods
    - [x] Initial research complete. No direct Takeout API exists.
    - [x] Investigate Data Portability API as the primary method.
    - [x] Document OAuth scope requirements for required data.
    - [x] Update architecture design with API strategy.
  - [ ] Facebook Data Download: Research automation methods
    - [x] Research complete. No direct API exists for personal data.
    - [x] Update architecture to reflect manual download guide strategy.
    - [ ] Create `docs/facebook_guide.md` with instructions.
    - [ ] Implement `FacebookProvider` to display the guide and link.
- [ ] Implement Twitter/X archive provider
- [ ] Implement LinkedIn data export provider

### Documentation

- [ ] Create developer documentation
- [ ] Write user guide with examples
- [ ] Document each provider's capabilities and limitations
- [ ] Add docstrings to all modules and functions

### Testing

- [ ] Set up pytest framework
- [ ] Create mock data for testing
- [ ] Implement unit tests for core functionality
- [ ] Implement integration tests for providers

## Notes

- All providers must strictly follow the platform's TOS
- Focus on user experience and clear documentation
- Ensure proper error handling and helpful user messages
- Consider rate limiting to avoid API abuse

### Provider Implementation

- [x] Google Provider: Initial research and setup complete.
- [ ] Facebook Data Download: Research automation methods

### Provider Implementation

- [ ] **Implement Google provider using Data Portability API** `BLOCKED`
  - [ ] Set up Google Cloud Project and OAuth credentials (Requires user action)
  - [ ] Implement OAuth 2.0 flow for user consent
  - [ ] Fetch data from a sample endpoint (e.g., `myactivity.youtube`)
  - [ ] Save fetched data using DataHandler
