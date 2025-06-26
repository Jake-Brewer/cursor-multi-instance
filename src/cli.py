# <!-- LOCKED:DIA:2023-05-28T15:50:00Z:2023-05-28T15:55:00Z -->
import click

from src.core.ingestor import Ingestor


@click.group()
def cli():
    """A command-line tool to ingest personal data from various sources."""
    pass


@cli.command()
def list_providers():
    """Lists all available data providers."""
    ingestor = Ingestor()
    ingestor.list_providers()


@cli.command()
@click.argument("provider_name")
def run(provider_name: str):
    """
    Runs the data ingestion for a specific provider.

    PROVIDER_NAME: The name of the provider to run (e.g., 'google').
    """
    ingestor = Ingestor()
    ingestor.run_provider(provider_name)


if __name__ == "__main__":
    cli()
