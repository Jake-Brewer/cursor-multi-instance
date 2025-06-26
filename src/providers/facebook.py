# <!-- LOCKED:DIA:2025-06-26T18:52:00Z:2025-06-26T18:57:00Z -->
from src.providers.base import BaseProvider


class FacebookProvider(BaseProvider):
    """
    Provider for guiding the user through a manual Facebook data download.
    """

    @property
    def provider_name(self) -> str:
        return "facebook"

    def authenticate(self) -> None:
        """Facebook authentication is handled by the user in their browser."""
        print("Facebook data must be downloaded manually.")
        pass

    def fetch_data(self) -> dict:
        """
        This method guides the user to the manual download instructions.
        """
        print("\\n" + "=" * 80)
        print("FACEBOOK DATA INGESTION - MANUAL STEPS REQUIRED")
        print("=" * 80)
        print("\\n1. This tool cannot automate your Facebook data download.")
        print("2. You must download your data archive from Facebook directly.")
        print(
            "3. Please follow the instructions in `docs/facebook_guide.md` "
            "to download your data in the correct format (JSON)."
        )
        print("\\n   Direct link: https://www.facebook.com/dyi/")
        print(
            "\\n4. Once downloaded, place the unzipped folder in the "
            "`input/facebook/` directory."
        )
        print("\\nA future feature will process this downloaded data.")
        print("\\n" + "=" * 80)
        return {"status": "manual_download_required", "guide": "docs/facebook_guide.md"}
