"""example is an example Python library and tool.

Divide one integer by another and log the result. Also log some information
from an environment variable and a package resource.

EXIT STATUS
    This utility exits with one of the following values:
    0   Calculation completed successfully.
    >0  An error occurred.
"""

# Standard Python Libraries
from collections.abc import MutableMapping
from importlib.resources import files
import logging
import os
import sys
from typing import Any

# Third-Party Libraries
import click
from rich.logging import RichHandler

from ._version import __version__

DEFAULT_ECHO_MESSAGE: str = "Hello World from the example default!"
LOG_LEVELS: list[str] = list()
if sys.version_info >= (3, 11):
    LOG_LEVELS = [*logging.getLevelNamesMapping()]
else:
    # The logging.getLevelNamesMapping method was only introduced in
    # Python 3.11.
    LOG_LEVELS = [
        logging.getLevelName(x)
        for x in range(0, 101)
        if not logging.getLevelName(x).startswith("Level")
    ]
# Context settings for click
CONTEXT_SETTINGS: MutableMapping[str, Any] = dict(help_option_names=["-h", "--help"])


def divide(dividend: int, divisor: int) -> float:
    """Divide dividend by divisor, log messages at various levels, and return the quotient."""
    logging.debug("This is a debug message")
    logging.info("This is an info message")
    logging.warning("This is a warning message")
    logging.error("This is an error message")
    logging.critical("This is a critical message")
    return dividend / divisor


def divisor_callback(ctx: click.Context, param: click.Parameter, value: int):
    """Verify that the value is nonzero."""
    if value == 0:
        raise click.BadParameter("divisor must be nonzero")

    return value


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("dividend", type=click.INT)
@click.argument("divisor", callback=divisor_callback, type=click.INT)
@click.option(
    "-l",
    "--log-level",
    default="info",
    help="The logging level.",
    type=click.Choice(LOG_LEVELS, case_sensitive=False),
)
@click.version_option(version=__version__, message="%(version)s")
def setup_logging_and_divide(
    dividend: int,
    divisor: int,
    log_level: str = "info",
) -> None:
    """Set up logging and call the division function.

    DIVIDEND is the integer dividend.
    DIVISOR is the nonzero integer divisor.
    """
    # Set up logging
    logging.basicConfig(
        format="%(asctime)-15s %(levelname)s %(message)s",
        level=log_level.upper(),
        handlers=[RichHandler(rich_tracebacks=True)],
    )

    logging.info("%d / %d == %f", dividend, divisor, divide(dividend, divisor))

    # Access some data from an environment variable
    message: str = os.getenv("ECHO_MESSAGE", DEFAULT_ECHO_MESSAGE)
    logging.info('ECHO_MESSAGE="%s"', message)

    # Access some data from our package data (see pyproject.toml)
    secret_message: str = (
        files(__package__).joinpath("data", "secret.txt").read_text().strip()
    )
    logging.info('Secret="%s"', secret_message)

    # Stop logging and clean up
    logging.shutdown()


def main() -> None:
    """Run the CLI."""
    setup_logging_and_divide()
