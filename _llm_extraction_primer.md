# Project Extraction Primer
# Last Updated: 2025-06-16T14:30:00Z

**AUDIENCE:** For LLMs (Claude, Grok, ChatGPT, etc.) - Guidelines for extracting components

## Purpose

This primer defines standards for extracting components from a project into standalone modules. It establishes best practices for planning, executing, and verifying extractions while maintaining functionality and integration points.

## Extraction Process

1. **Pre-Extraction Planning**:
   - Document component boundaries and dependencies
   - Identify integration points between components
   - Create inventory of files to be extracted
   - Determine target directory structure
   - Define clear APIs between components

2. **Component Extraction**:
   - Create peer-level directories for extracted components
   - Move files to appropriate locations
   - Update import paths and references
   - Create FOLDER_GUIDE.md files in all directories
   - Maintain consistent code style and conventions

3. **Integration Implementation**:
   - Implement client libraries for cross-component communication
   - Document authentication and error handling
   - Create integration tests
   - Define fallback mechanisms for graceful degradation

4. **Verification**:
   - Verify functionality of extracted components
   - Test integration points between components
   - Confirm all files have been properly moved
   - Check for any remaining references to old locations
   - Ensure documentation is complete and accurate

5. **Cleanup**:
   - Remove original directories after successful extraction
   - Update documentation to reflect new structure
   - Remove temporary files created during extraction
   - Create final extraction report
   - Announce completion of extraction

## Directory Structure

1. **Peer-Level Organization**:
   - Place extracted components at the same directory level as the original project
   - Use consistent naming conventions for all components
   - Example:
     ```
     /project-root/
     ├── original-project/
     ├── extracted-component-1/
     └── extracted-component-2/
     ```

2. **Component Structure**:
   - Maintain consistent internal structure across components
   - Include standard directories (src/, tests/, docs/, etc.)
   - Create FOLDER_GUIDE.md files in all directories

## Integration Standards

1. **API Design**:
   - Define clear, stable APIs between components
   - Use versioning for breaking changes
   - Document all public interfaces
   - Implement proper error handling

2. **Communication Patterns**:
   - Use appropriate communication patterns (REST, WebSockets, etc.)
   - Implement authentication and authorization
   - Include retry logic with exponential backoff
   - Document rate limits and timeout settings

3. **Configuration Management**:
   - Use environment variables for deployment-specific settings
   - Store configuration in standard locations
   - Document all configuration options
   - Provide sensible defaults

## Documentation Requirements

1. **Extraction Documentation**:
   - Document the extraction process
   - Record decisions made during extraction
   - Note any issues encountered and their resolutions
   - Include before/after diagrams of component relationships

2. **Integration Documentation**:
   - Create detailed integration guides
   - Document all API endpoints
   - Include code examples
   - Describe error scenarios and handling

3. **FOLDER_GUIDE.md Files**:
   - Create FOLDER_GUIDE.md files in all directories
   - Follow the format specified in _llm_primer.md
   - Update in real-time as files are added or modified

## Best Practices

1. **Incremental Extraction**:
   - Extract one component at a time
   - Verify functionality after each extraction
   - Address issues before moving to the next component
   - Document lessons learned for future extractions

2. **Code Quality**:
   - Maintain or improve code quality during extraction
   - Fix bugs encountered during extraction
   - Refactor code as needed for clean separation
   - Ensure consistent code style

3. **Testing**:
   - Create tests for integration points
   - Verify functionality before and after extraction
   - Use automated tests where possible
   - Document manual testing procedures

Remember: This primer works in conjunction with the core _llm_primer.md and may be overridden by project-specific instructions in _llm_project_primer.md.
