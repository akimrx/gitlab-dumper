import click

from src._settings import get_settings, get_logger
from src._gitlab import get_gitlab_client

logger = get_logger()
gitlab = get_gitlab_client(get_settings())


@click.group("projects")
def projects_cli_commands() -> None:
    """Operations with Gitlab projects."""


@projects_cli_commands.command("list")
def projects() -> None:
    """Show available Gitlab projects."""
    available_projects = gitlab.fetch_available_projects()
    print(len(list(available_projects)))
