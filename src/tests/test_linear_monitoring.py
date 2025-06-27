import signal
import pytest
from unittest.mock import Mock, patch
from src.core.monitor import LinearTaskMonitor


class TestLinearTaskMonitor:
    @pytest.fixture
    def mock_linear_client(self):
        """Create a mock Linear client for testing."""
        client = Mock()
        client.list_issues.return_value = []
        return client

    def test_monitor_initialization(self, mock_linear_client):
        """Test monitor initialization with default parameters."""
        monitor = LinearTaskMonitor(
            linear_client=mock_linear_client, poll_interval=5, max_retries=3
        )

        assert monitor.poll_interval == 5
        assert monitor.max_retries == 3
        assert monitor.current_retry == 0

    def test_adaptive_polling_backoff(self, mock_linear_client):
        """Test adaptive polling with exponential backoff."""
        monitor = LinearTaskMonitor(
            linear_client=mock_linear_client,
            poll_interval=1,
            max_retries=3,
            backoff_factor=2,
        )

        # Simulate failed attempts
        monitor.current_retry = 2
        next_interval = monitor._calculate_next_interval()

        assert next_interval == 1 * (2**2)  # 1 * 2^2 = 4 seconds

    @patch("time.sleep")
    def test_monitoring_loop_error_handling(self, mock_sleep, mock_linear_client):
        """Test error handling in monitoring loop."""
        # Simulate intermittent network errors
        mock_linear_client.list_issues.side_effect = [
            ConnectionError("Network error"),
            ConnectionError("Network error"),
            [],  # Successful fetch on third attempt
        ]

        monitor = LinearTaskMonitor(
            linear_client=mock_linear_client, poll_interval=1, max_retries=3
        )

        # Run monitoring loop
        with pytest.raises(ConnectionError, match="Max retries exceeded"):
            monitor.start_monitoring()

        # Verify retry mechanism
        assert mock_linear_client.list_issues.call_count == 3
        assert monitor.current_retry == 3

    def test_task_processing_filter(self, mock_linear_client):
        """Test filtering and processing of Linear tasks."""
        # Create mock tasks with different states
        mock_tasks = [
            Mock(state="backlog", priority=2),
            Mock(state="in_progress", priority=1),
            Mock(state="done", priority=3),
        ]
        mock_linear_client.list_issues.return_value = mock_tasks

        monitor = LinearTaskMonitor(linear_client=mock_linear_client, poll_interval=5)

        # Process tasks with custom filtering
        processed_tasks = monitor._filter_tasks(
            tasks=mock_tasks,
            state_filter=["backlog", "in_progress"],
            priority_threshold=2,
        )

        assert len(processed_tasks) == 1
        assert processed_tasks[0].state == "backlog"
        assert processed_tasks[0].priority == 2

    def test_graceful_shutdown(self, mock_linear_client):
        """Test graceful shutdown of monitoring loop."""
        monitor = LinearTaskMonitor(linear_client=mock_linear_client, poll_interval=1)

        # Simulate shutdown signal
        with patch("signal.signal") as mock_signal:
            monitor.start_monitoring(timeout=10)
            mock_signal.assert_called_with(signal.SIGINT, monitor._handle_shutdown)
