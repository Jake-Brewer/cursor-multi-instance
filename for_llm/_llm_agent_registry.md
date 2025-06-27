# LLM Agent Registry
<!-- Updated: 2024-07-10T12:00:00Z -->

This file tracks active LLM agents working in this repository to prevent conflicts.

## Active Agents

| Agent Name | Prefix | Created | Last Seen | Scope |
|------------|--------|---------|-----------|-------|
| DataIngestorAgent | DIA | 2023-05-28T14:32:45Z | 2023-05-28T14:32:45Z | Setting up Python project for personal data ingestion |
| LinearTaskProcessor | LTP | 2023-06-14T15:21:00Z | 2025-06-27 05:41:59 | Processing Linear issues (label management, decomposition) |
| TaskExecutor | TE | 2023-06-21T11:00:00Z | 2023-06-21T11:00:00Z | Executing Linear tasks for the data-ingestor project |
| MonitoringAgent | MA | 2024-07-10T12:00:00Z | 2024-07-10T12:00:00Z | Implementing task monitoring and Linear task processing |
| AutonomousReadyToWorkExecutor | ARTWE | 2025-06-27T05:45:00Z | 2025-06-27T05:45:00Z | Autonomously executing ready-to-work Linear tasks |
| ContinuousDesignDetailingAgent | CDDA | 2025-06-27T06:00:00Z | 2025-06-27T06:00:00Z | Converting needs-design issues into fully specified tickets ready for implementation |

## Registration Process

1. Agents must register here before performing work
2. Update your "Last Seen" timestamp regularly
3. When locking files, use your prefix in the format: `<!-- LOCKED:[PREFIX]:[TIMESTAMP]:[EXPIRES] -->`
4. Locks expire after 5 minutes or with the next git commit
5. Never edit files locked by another agent unless the lock is expired
