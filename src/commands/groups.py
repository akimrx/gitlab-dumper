import click
from tabulate import tabulate

from src._settings import get_settings, get_logger
from src._gitlab import get_gitlab_client

logger = get_logger()
gitlab = get_gitlab_client(get_settings())


@click.group("groups")
def groups_cli_commands() -> None:
    """Operations with Gitlab groups."""


@groups_cli_commands.command("list")
@click.option("--parents", "parents_only", is_flag=True, default=False, help="Show only parent groups.")
@click.option("--exclude", required=False, type=str, default=None, help="Comma-separated groups to exclude.")
def groups(parents_only: bool, exclude: str | None = None) -> None:
    """Show available Gitlab groups."""

    if exclude is not None:
        exclude = list(map(lambda item: item.strip(), exclude.split(",")))

    available_groups = gitlab.fetch_available_groups(only_parent_groups=parents_only, exclude=exclude)

    headers = ["id", "name", "slug", "url"]
    table_data = list(map(lambda group: [group.id, group.name, group.path, group.web_url], available_groups))
    table = tabulate(table_data, headers=headers)

    click.echo("")
    click.echo(table)
