import sys
import click

from src import __version__
from src._settings import get_settings, get_logger

settings = get_settings()
logger = get_logger()


@click.group()
@click.version_option(__version__)
def cli() -> None:
    """Gitlab dumper CLI."""


def main() -> None:
    """CLI entrypoint."""
    try:
        from src.commands.projects import projects_cli_commands
        from src.commands.groups import groups_cli_commands

        cli.add_command(projects_cli_commands)
        cli.add_command(groups_cli_commands)
        cli()
    except Exception as e:
        click.secho(f"{e.__class__.__name__}: {str(e)}", bold=True, fg="red", file=sys.stderr)
        if settings.LOG_LEVEL.lower() == "debug":
            raise


if __name__ == "__main__":
    main()
