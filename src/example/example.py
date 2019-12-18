#!/usr/bin/env python

"""example is an example Python library and tool.

Usage:
  example [--log-level=LEVEL]
  example (-h | --help)

Options:
  -h --help              Show this message.
  --log-level=LEVEL      If specified, then the log level will be set to
                         the specified value.  Valid values are "debug", "info",
                         "warning", "error", and "critical". [default: warning]
"""

# standard python libraries
import logging
import os
import sys

# third-party libraries
import docopt
import pkg_resources

from ._version import __version__

DEFAULT_ECHO_MESSAGE = "Hello World from the example default!"


def example_div(x, y):
    """Print some logging messages."""
    logging.debug("This is a debug message")
    logging.info("This is an info message")
    logging.warning("This is a warning message")
    logging.error("This is an error message")
    logging.critical("This is a critical message")
    return x / y


def main():
    """Set up logging and call the example function."""
    args = docopt.docopt(__doc__, version=__version__)
    # Set up logging
    log_level = args["--log-level"]
    try:
        logging.basicConfig(
            format="%(asctime)-15s %(levelname)s %(message)s", level=log_level.upper()
        )
    except ValueError:
        logging.critical(
            f'"{log_level}" is not a valid logging level.  Possible values '
            "are debug, info, warning, and error."
        )
        return 1

    print(f"8 / 2 == {example_div(8, 2)}")

    # Access some data from an environment variable
    message = os.getenv("ECHO_MESSAGE", DEFAULT_ECHO_MESSAGE)
    print(f'ECHO_MESSAGE="{message}"')

    # Access some data from our package data (see the setup.py)
    secret_message = (
        pkg_resources.resource_string("example", "data/secret.txt")
        .decode("utf-8")
        .strip()
    )
    print(f'Secret="{secret_message}"')

    # Stop logging and clean up
    logging.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
