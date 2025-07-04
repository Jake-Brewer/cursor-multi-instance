# Multi-Agent Collaboration Primer
# Last Updated: 2025-06-16T14:30:00Z

**AUDIENCE:** For LLMs (Claude, Grok, ChatGPT, etc.) - Guidelines for multi-agent collaboration

## Purpose

This primer defines standards for collaboration between multiple AI agents working on the same project. It establishes communication protocols, task management, and coordination mechanisms to ensure efficient teamwork.

## Communication Structure

1. **Message Format**:
   ```
   # Message Title

   Message-ID: <unique-identifier>
   Created: YYYY-MM-DDThh:mm:ss-TZ
   From: <agent-name>
   To: <agent-name>
   Authority: lead|contributor|peer
   Purpose: instruction|status|question|response
   Status: unread|read|actioned
   Task: <task-identifier>
   Relevance: until-<event-that-makes-message-obsolete>

   ## Content

   Your message here...

   ## Metadata
   Priority: low|normal|high|urgent
   References: related-message-ids
   ```

2. **Directory Structure**:
   - Store messages in `_for_llm/shared/interfaces/inbox/<to-agent>/`
   - Use filename format: `<from-agent>_YYYYMMDD-HHMMSS_<brief-description>.md`
   - Example: `agent-docker-command_20250616-143000_task-assignment.md`

3. **Authority Model**:
   - Designate one agent as the "lead" with final decision-making authority
   - Contributors provide input but defer to lead agent on conflicts
   - Peer relationships for agents with separate domains of responsibility

## Task Management

1. **Task Assignment**:
   - Include task identifier in message header
   - Clearly define acceptance criteria for each task
   - Link related messages in task metadata
   - Update task status: assigned → in-progress → review → complete

2. **Task Completion**:
   - Mark messages as obsolete when the associated task is complete
   - Document any issues encountered during task execution
   - Include task identifier in completion messages

## Agent Lifecycle

1. **Agent Initialization**:
   - Announce presence and capabilities
   - Request task assignments
   - Establish authority relationships

2. **Agent Retirement**:
   - Submit retirement message when all tasks are complete
   - Include summary of accomplishments
   - Document what worked well and what did not
   - Explain why retirement is appropriate

## Conflict Resolution

1. **When Agents Disagree**:
   - Document different perspectives with reasoning
   - Defer to lead agent for final decision
   - Record decision rationale for future reference
   - Implement decided approach without further debate

2. **When Instructions Conflict**:
   - Prioritize most recent instructions
   - Request clarification when conflicts cannot be resolved
   - Document conflicts and resolutions for future reference

## Parallel Processing

1. **Task Parallelization**:
   - Identify independent tasks that can be executed simultaneously
   - Divide work among agents based on capabilities
   - Use exponential backoff for failed operations
   - Monitor resource usage when running parallel operations

2. **Coordination**:
   - Use status messages to coordinate dependencies
   - Help other agents when your tasks are complete
   - Adapt to failures by trying alternative approaches

## Best Practices

1. **Message Management**:
   - Keep messages focused on a single topic or task
   - Use clear, descriptive titles
   - Include all necessary context within the message
   - Reference previous messages when continuing a conversation

2. **Error Handling**:
   - Document errors encountered during task execution
   - Implement exponential backoff for failed operations
   - Share solutions to common problems
   - Help other agents troubleshoot issues

Remember: This primer works in conjunction with the core _llm_primer.md and may be overridden by project-specific instructions in _llm_project_primer.md.
