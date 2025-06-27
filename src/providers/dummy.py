from src.providers.base import BaseProvider


class DummyProvider(BaseProvider):
    """
    A dummy provider for testing the framework.
    It does not connect to any external service.
    """

    @property
    def provider_name(self) -> str:
        return "dummy"

    def authenticate(self) -> None:
        """Dummy authentication method."""
        print("Authenticating with dummy provider...")
        # No actual authentication needed
        pass

    def fetch_data(self) -> dict:
        """Dummy data fetching method."""
        print("Fetching data from dummy provider...")
        return {
            "user_id": 12345,
            "username": "dummy_user",
            "data": "This is mock data from the dummy provider.",
        } 