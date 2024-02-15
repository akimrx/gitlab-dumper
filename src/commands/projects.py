import click
import time

from tabulate import tabulate
from gitlab.v4.objects import Project

from src._settings import get_settings, get_logger
from src._gitlab import get_gitlab_client
from src._git import clone_or_update_repo, save_repo_as_archive
from src._utils import bytes_to_human

settings = get_settings()
logger = get_logger()
gitlab = get_gitlab_client(settings)


@click.group("projects")
def projects_cli_commands() -> None:
    """Operations with Gitlab projects."""


@projects_cli_commands.command("list")
@click.option("--no-personal", "no_personal", is_flag=True, default=False, help="Hide personal user projects.")
def projects_list(no_personal: bool) -> None:
    """Show available Gitlab projects."""
    available_projects = gitlab.fetch_available_projects(statistics=True, no_personal=no_personal)

    def get_project_size(project: Project) -> str:
        size = project.statistics.get("repository_size", 0)
        return bytes_to_human(size)

    headers = ["repo", "size", "kind", "url"]
    table_data = map(
        lambda p: [p.path_with_namespace, get_project_size(p), p.namespace.get("kind", "–"), p.web_url],
        available_projects,
    )
    table = tabulate(table_data, headers=headers)

    click.echo("")
    click.echo(table)


@projects_cli_commands.command("dump")
@click.option(
    "--dumps-dir",
    "dumps_dir",
    required=False,
    type=str,
    default=settings.DEFAULT_DUMP_DIR,
    help=f"Directory for dumps (default: {settings.DEFAULT_DUMP_DIR}).",
)
@click.option("--delay", required=False, type=int, default=0, help="Delay between clones in seconds (default 0).")
@click.option("--skip-empty", "skip_empty", is_flag=True, default=False, help="Ignore empty projects.")
@click.option("--no-personal", "no_personal", is_flag=True, default=False, help="Ignore personal user projects.")
@click.option(
    "--as-archive",
    "as_archive",
    is_flag=True,
    default=False,
    help="Download projects as tar.gz archive instead clone.",
)
@click.option("--dry-run", "dry_run", is_flag=True, default=False, help="Safe simulate dump without download/clone.")
@click.option("--namespaces", required=False, type=str, default=None, help="Comma-separated namespaces to operate.")
@click.option("--exclude", required=False, type=str, default=None, help="Comma-separated projects (slug) to exclude.")
def projects_dump(
    dumps_dir: str,
    delay: int,
    skip_empty: bool,
    no_personal: bool,
    as_archive: bool,
    dry_run: bool,
    namespaces: list[str] | None = None,
    exclude: list[str] | None = None,
) -> None:
    """Download, clone or re-pull all available projects. All flags are optional."""

    if exclude is not None:
        exclude = list(map(lambda item: item.strip().lower(), exclude.split(",")))

    if namespaces is not None:
        namespaces = list(map(lambda item: item.strip().lower(), namespaces.split(",")))

    no_matches = True  # hack: for UX friendly message, cause we works with iterators/generators
    failed_projects: list[list[str]] = []
    all_available_projects = gitlab.fetch_available_projects(
        exclude=exclude, namespaces=namespaces, no_personal=no_personal
    )

    for project in all_available_projects:
        no_matches = False
        if project.empty_repo and skip_empty:
            logger.info(f"Repo {project.path_with_namespace} is empty, ignoring")
            continue

        try:
            if as_archive:
                save_repo_as_archive(project, dumps_base_dir=dumps_dir, dry_run=dry_run)
            else:
                clone_or_update_repo(project, dumps_base_dir=dumps_dir, dry_run=dry_run)
        except Exception as e:
            error_msg = f"{e.__class__.__name__}: {str(e)}"
            failed_projects.append([project.path_with_namespace, error_msg])

            logger.error(f"Something went wrong while clone or pull repo {project.path_with_namespace}")
            logger.exception(e)

        if delay > 0:
            if dry_run:
                logger.info(f"Simulate delay for {delay}s before next step")
            else:
                logger.info(f"Waiting delay ({delay}s) before next {'download' if as_archive else 'clone'}...")
                time.sleep(delay)

    if failed_projects:
        headers = ["repo", "error"]
        table = tabulate(failed_projects, headers=headers)

        click.echo("")
        click.secho(f"{len(failed_projects)} project has failed", fg="red")
        click.echo("")
        click.echo(table)

    if no_matches:
        click.secho("Projects by params not found.", bold=True, fg="yellow")
