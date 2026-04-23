"""example is an example Python library and tool.

Divide one integer by another and log the result. Also log some information
from an environment variable and a package resource.
"""

# Standard Python Libraries
from dataclasses import dataclass
from importlib.resources import files
import logging
import os
from typing import Annotated, Literal

# Third-Party Libraries
import cappa

from ._version import __version__

DEFAULT_ECHO_MESSAGE: str = "Hello World from the example default!"


@dataclass
class Example:
    """example is an example Python library and tool.

    Divide one integer by another and log the result. Also log some information
    from an environment variable and a package resource.
    """

    dividend: Annotated[int, cappa.Arg(help="The dividend. Must be an integer.")]
    divisor: Annotated[int, cappa.Arg(help="The divisor. Must be a non-zero integer.")]
    log_level: Annotated[
        Literal["debug", "info", "warning", "error", "critical"],
        cappa.Arg(
            help="If specified, then the log level will be set to the specified value.",
            long=True,
        ),
    ] = "info"

    def __post_init__(self):
        """Perform any validation of inputs."""
        if self.divisor == 0:
            raise ValueError("'divisor' must be an integer that is not 0.")


def example_div(dividend: int, divisor: int) -> float:
    """Print some logging messages."""
    logging.debug("This is a debug message")
    logging.info("This is an info message")
    logging.warning("This is a warning message")
    logging.error("This is an error message")
    logging.critical("This is a critical message")
    return dividend / divisor


def main() -> None:
    """Set up logging and call the example function."""
    args: Example = cappa.parse(Example, completion=False, version=__version__)

    # Set up logging
    logging.basicConfig(
        format="%(asctime)-15s %(levelname)s %(message)s", level=args.log_level.upper()
    )

    logging.info(
        "%d / %d == %f",
        args.dividend,
        args.divisor,
        example_div(args.dividend, args.divisor),
    )

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
