import click
from tabulate import tabulate

from src._settings import get_settings, get_logger
from src._gitlab import get_gitlab_client, Group

logger = get_logger()
gitlab = get_gitlab_client(get_settings())


@click.group("groups")
def groups_cli_commands() -> None:
    """Operations with Gitlab groups."""


@groups_cli_commands.command("list")
@click.option("--parents", "parents_only", is_flag=True, default=False, help="Show only parent groups.")
@click.option("--subgroups", "subgroups", is_flag=True, default=False, help="Also show subgroups.")
@click.option("--exclude", required=False, type=str, default=None, help="Comma-separated groups to exclude.")
def list_groups(parents_only: bool, subgroups: bool, exclude: str | None = None) -> None:
    """Show available Gitlab groups."""

    if exclude is not None:
        exclude = list(map(lambda item: item.strip().lower(), exclude.split(",")))

    available_groups = gitlab.fetch_available_groups(only_parent_groups=parents_only, exclude=exclude)

    def with_subgroup_formatter(group: Group) -> list[str]:
        subgroups = group.subgroups.list(all=True, iterator=True)

        return [
            group.id,
            group.path,
            group.full_path,
            ", ".join(map(lambda sg: sg.path, subgroups)) or "—",
        ]

    if subgroups:
        headers = ["id", "slug", "fully qualified slug", "subgroups"]
        table_data = map(with_subgroup_formatter, available_groups)
    else:
        headers = ["id", "slug", "fully qualified slug", "url"]
        table_data = map(lambda g: [g.id, g.path, g.full_path, g.web_url], available_groups)

    table = tabulate(table_data, headers=headers)

    click.echo("")
    click.echo(table)


@groups_cli_commands.command("projects")
@click.argument("slug")
def list_group_projects(slug: str) -> None:
    """
    List projects in group or subgroup.
    Slug must be passed as fully qualified path.
    """

    group = gitlab.client.groups.get(slug)
    group_projects = group.projects.list(all=True, iterator=True)

    headers = ["id", "slug", "fully qualified slug", "url"]
    table_data = map(lambda p: [p.id, p.path, p.path_with_namespace, p.web_url], group_projects)
    table = tabulate(table_data, headers=headers)

    click.echo("")
    click.echo(table)
