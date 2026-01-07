"""example is an example Python library and tool.

Divide one integer by another and log the result. Also log some information
from an environment variable and a package resource.

EXIT STATUS
    This utility exits with one of the following values:
    0   Calculation completed successfully.
    >0  An error occurred.
"""

# Standard Python Libraries
from importlib.resources import files
import logging
import os
import sys
from typing import Annotated

# Third-Party Libraries
from rich import print
from rich.logging import RichHandler
import typer

from ._version import __version__

DEFAULT_ECHO_MESSAGE: str = "Hello World from the example default!"
LOG_LEVELS: list[str] = list()
if sys.version_info.minor > 10:
    LOG_LEVELS = [*logging.getLevelNamesMapping()]
else:
    # The logging.getLevelNamesMapping method was only introduced in
    # Python 3.11.
    LOG_LEVELS = [
        logging.getLevelName(x)
        for x in range(0, 101)
        if not logging.getLevelName(x).startswith("Level")
    ]

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


def example_div(dividend: int, divisor: int) -> float:
    """Print some logging messages."""
    logging.debug("This is a debug message")
    logging.info("This is an info message")
    logging.warning("This is a warning message")
    logging.error("This is an error message")
    logging.critical("This is a critical message")
    return dividend / divisor


def divisor_callback(value: int) -> int:
    """Verify that the divisor is not zero."""
    if value == 0:
        raise typer.BadParameter("divisor must not be zero")
    return value


def log_level_callback(value: str) -> str:
    """Verify that the value is a valid logging level name."""
    if value.upper() not in LOG_LEVELS:
        raise typer.BadParameter(
            f"log_level must one of the following:  {', '.join(LOG_LEVELS)}"
        )
    return value


def version_callback(ctx: typer.Context, value: bool) -> None:
    """If value is True then print the version and exit early."""
    # Doing this doesn't break shell completion when you print text to
    # the screen from a callback.  For more information see:
    # https://typer.tiangolo.com/tutorial/options/callback-and-context/#fix-completion-using-the-context
    if ctx.resilient_parsing:
        return

    if value:
        print(__version__)
        raise typer.Exit()


@app.command()
def example(
    dividend: Annotated[int, typer.Argument(help="The dividend")],
    divisor: Annotated[
        int, typer.Argument(callback=divisor_callback, help="The nonzero divisor")
    ],
    log_level: Annotated[
        str,
        typer.Option(
            callback=log_level_callback,
            help=f"The logging level.  Valid values are:  {', '.join(LOG_LEVELS)}.",
        ),
    ] = "info",
    version: Annotated[
        bool | None,
        typer.Option(
            "--version", callback=version_callback, help="Show version", is_eager=True
        ),
    ] = None,
) -> None:
    """Set up logging and call the division function."""
    # Set up logging
    logging.basicConfig(
        format="%(asctime)-15s %(levelname)s %(message)s",
        level=log_level.upper(),
        handlers=[RichHandler(rich_tracebacks=True)],
    )

    logging.info("%d / %d == %f", dividend, divisor, example_div(dividend, divisor))

    # Access some data from an environment variable
    message: str = os.getenv("ECHO_MESSAGE", DEFAULT_ECHO_MESSAGE)
    logging.info('ECHO_MESSAGE="%s"', message)

    # Access some data from our package data (see the setup.py)
    secret_message: str = (
        files(__package__).joinpath("data", "secret.txt").read_text().strip()
    )
    logging.info('Secret="%s"', secret_message)

    # Stop logging and clean up
    logging.shutdown()


def main() -> None:
    """Run the CLI."""
    app()
