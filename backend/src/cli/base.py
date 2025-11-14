import click


@click.group()
def cli() -> None:
    """Entry point for the command-line tool app.

    This is the main command group that provides access to all available commands.
    """
