#!/usr/bin/env python3
"""
Task Monitor Script with Adaptive Polling and Exponential Backoff

This script checks for Linear tasks labeled "ready-to-work" with a dynamic delay.
- It shortens the delay on successful checks.
- It increases the delay (exponential backoff) on errors.
- It terminates if no tasks are found for a cumulative 10 minutes.
"""

import sys
import time
import logging
import json
import subprocess
import datetime
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

# --- Constants ---
PROJECT_ID = "3d3a7b29-3f92-4d11-92d9-9e87c3c2bb81"
LABEL_QUERY = 'label:"ready-to-work"'
TODO_FILE = "for_llm_todo_TaskExecutor.md"

# --- Initialization (Rule 1) ---
INITIAL_DELAY = 30.0  # seconds
MIN_DELAY = 5.0  # seconds
MAX_DELAY = 60 * 60.0  # 1 hour
BACKOFF_FACTOR = 2.0
SUCCESS_SHORTENING_FACTOR = 0.9
TERMINATION_THRESHOLD = 10 * 60  # 10 minutes in seconds


def run_linear_query(project_id, query):
    """
    Runs a Linear query to find issues.
    Returns the parsed JSON response on success, raises Exception on failure.
    """
    cmd = [
        "curl",
        "-s",
        "http://localhost:5005/mcp/mcp_linear-oauth_list_issues",
        "-H",
        "Content-Type: application/json",
        "-d",
        json.dumps({"projectId": project_id, "query": query}),
    ]

    try:
        # Using subprocess.run for better control and error handling
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True, shell=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        # This will be caught as an exception in the main loop
        raise Exception(
            f"Linear query failed with exit code {e.returncode}: {e.stderr}"
        )
    except json.JSONDecodeError:
        # Handle cases where the output is not valid JSON
        raise Exception("Failed to decode JSON response from Linear query.")


def update_log(message):
    """Appends a message to the monitoring log in the TODO file."""
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    log_entry = f"| {timestamp} | {message} |\n"

    # This is a simplified way to append to a specific part of a markdown file.
    # A more robust implementation would parse the markdown.
    try:
        with open(TODO_FILE, "a") as f:
            f.write(log_entry)
    except IOError as e:
        print(f"Warning: Could not write to log file {TODO_FILE}: {e}")


def main():
    """Main monitoring loop."""
    current_delay = INITIAL_DELAY
    no_task_duration = 0.0

    update_log(f"Monitoring started. Initial delay: {current_delay:.1f}s")
    print(
        f"Monitoring started. Initial delay: {current_delay:.1f}s. "
        f"Will terminate after {TERMINATION_THRESHOLD / 60:.0f} mins "
        "of no tasks."
    )

    while True:
        # --- Monitoring Cycle (Rule 2) ---
        print(f"\nWaiting for {current_delay:.2f} seconds...")
        time.sleep(current_delay)

        try:
            # Attempt to query Linear
            response = run_linear_query(PROJECT_ID, LABEL_QUERY)
            issues = response.get("results", [])

            # --- On Query Success (Rule 3) ---
            if issues:
                print(f"SUCCESS: Found {len(issues)} 'ready-to-work' task(s).")
                for issue in issues:
                    print(f"  - {issue.get('identifier')}: " f"{issue.get('title')}")
                update_log(f"Found {len(issues)} task(s). Handing off to worker.")

                # Handing off to the main agent to process the task
                break
            else:
                # No tasks found
                no_task_duration += current_delay
                print(
                    "SUCCESS: No 'ready-to-work' tasks found. "
                    f"Cumulative idle time: {no_task_duration:.2f}s"
                )
                new_delay = max(MIN_DELAY, current_delay * SUCCESS_SHORTENING_FACTOR)
                update_log(
                    f"No tasks found. Idle time: {no_task_duration:.1f}s. "
                    f"New delay: {new_delay:.1f}s"
                )

                # --- Termination Condition (Rule 5) ---
                if no_task_duration >= TERMINATION_THRESHOLD:
                    print(
                        "\nTermination condition met: No tasks found for "
                        f"{no_task_duration / 60:.2f} minutes."
                    )
                    update_log("Termination condition met. Concluding work.")
                    break

                # Shorten delay for next successful poll
                current_delay = new_delay

        except Exception as e:
            # --- On Query Failure (Rule 4) ---
            print(f"ERROR: Query failed: {e}")
            no_task_duration = 0  # Reset timer on failure

            # Increase delay using exponential backoff with jitter
            backoff = current_delay * BACKOFF_FACTOR
            jitter = random.uniform(0, 1)
            current_delay = min(MAX_DELAY, backoff + jitter)

            print(
                "Resetting idle timer. Applying exponential backoff. "
                f"New delay: {current_delay:.2f}s"
            )
            update_log(
                "Query ERROR. Reset idle time. " f"New delay: {current_delay:.1f}s"
            )


if __name__ == "__main__":
    main()
