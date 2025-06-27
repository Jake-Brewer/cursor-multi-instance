import signal
import time
from typing import List, Optional, Any


class LinearTaskMonitor:
    """Monitor Linear tasks with adaptive polling and error handling."""

    def __init__(
        self,
        linear_client: Any,
        poll_interval: int = 5,
        max_retries: int = 3,
        backoff_factor: float = 2.0,
    ):
        """
        Initialize the Linear task monitor.

        Args:
            linear_client: Client for interacting with Linear API
            poll_interval: Base interval between polling attempts
            max_retries: Maximum number of retry attempts
            backoff_factor: Factor for exponential backoff
        """
        self.linear_client = linear_client
        self.poll_interval = poll_interval
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.current_retry = 0

    def _calculate_next_interval(self) -> float:
        """
        Calculate the next polling interval using exponential backoff.

        Returns:
            Next polling interval in seconds
        """
        return self.poll_interval * (self.backoff_factor**self.current_retry)

    def _filter_tasks(
        self,
        tasks: List[Any],
        state_filter: Optional[List[str]] = None,
        priority_threshold: Optional[int] = None,
    ) -> List[Any]:
        """
        Filter tasks based on state and priority.

        Args:
            tasks: List of tasks to filter
            state_filter: List of allowed task states
            priority_threshold: Minimum priority for tasks

        Returns:
            Filtered list of tasks
        """
        filtered_tasks = tasks

        if state_filter:
            filtered_tasks = [
                task for task in filtered_tasks if task.state in state_filter
            ]

        if priority_threshold is not None:
            filtered_tasks = [
                task for task in filtered_tasks if task.priority >= priority_threshold
            ]

        return filtered_tasks

    def start_monitoring(
        self,
        state_filter: Optional[List[str]] = None,
        priority_threshold: Optional[int] = None,
        timeout: Optional[int] = None,
    ) -> None:
        """
        Start the monitoring loop with error handling.

        Args:
            state_filter: List of task states to monitor
            priority_threshold: Minimum task priority
            timeout: Maximum time to run monitoring loop
        """
        signal.signal(signal.SIGINT, self._handle_shutdown)

        start_time = time.time()

        while timeout is None or time.time() - start_time < timeout:
            try:
                tasks = self.linear_client.list_issues()
                filtered_tasks = self._filter_tasks(
                    tasks, state_filter, priority_threshold
                )

                # Process tasks here
                for task in filtered_tasks:
                    # Implement task processing logic
                    pass

                self.current_retry = 0
                time.sleep(self.poll_interval)

            except ConnectionError as e:
                self.current_retry += 1

                if self.current_retry > self.max_retries:
                    raise ConnectionError("Max retries exceeded") from e

                retry_interval = self._calculate_next_interval()
                time.sleep(retry_interval)

    def _handle_shutdown(self, signum: int, frame: Any) -> None:
        """
        Handle graceful shutdown of the monitoring loop.

        Args:
            signum: Signal number
            frame: Current stack frame
        """
        print("Monitoring loop interrupted. Shutting down gracefully.")
        exit(0)
