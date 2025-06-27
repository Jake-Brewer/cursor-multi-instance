import os
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from src.providers.base import BaseProvider


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class GmailProvider(BaseProvider):
    """A provider for fetching data from Google Gmail."""

    def __init__(self):
        super().__init__()
        self.creds: Credentials | None = None

    @property
    def provider_name(self) -> str:
        """The unique name of the provider."""
        return "gmail"

    def authenticate(self) -> None:
        """
        Handles authentication with Google's Gmail API using OAuth 2.0.
        """
        creds = None
        # token.json stores the user's access and refresh tokens.
        # It's created automatically when the auth flow completes.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # This requires a credentials.json file from Google Cloud.
                # See JAK-429 for details.
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        self.creds = creds
        print("Gmail authentication successful.")

    def fetch_data(self) -> Any:
        """
        Fetches emails and attachments from Gmail.

        This will be implemented later to use the Gmail API.
        """
        if not self.creds:
            print("Not authenticated. Please run authenticate() first.")
            return None

        print("Fetching data from Gmail...")
        # TODO: Implement data fetching from Gmail API
        return {"message": "Data from Gmail will be here."}
