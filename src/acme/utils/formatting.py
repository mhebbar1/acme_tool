"""Helpers for formatting text and data."""
# Standard Library
import logging
import sys

# Acme modules
from rich.console import Console
from rich.markup import escape

from acme.settings import LOG_FORMAT_STRING, LOG_LEVEL


class Symbols:
    """List of common symbols / emojis used for logging."""

    STEP_HEAVY_WIDE = '[dim] ➜ [/dim]'
    CHECK_HEAVY = '[green bold] ✔ [/green bold]'
    CHECK_FAIL_EMOJI = '[red bold] × [/red bold]'
    WARNING = '[yellow bold] ⚠ [/yellow bold]'


def colorize(text: str, color: str) -> str:
    """Colorize text for terminal output."""
    return f'[{color}]{text}[/{color}]'


def print_step(message: str, pad_above: bool = False):
    """Print a message with a step indicator."""
    if pad_above:
        logger.info('')

    logger.info(f'{Symbols.STEP_HEAVY_WIDE} [dim]{escape(message)}[/dim]')  # noqa: G004


def print_info(message: str, pad_above: bool = False):
    """Print an info message."""
    if pad_above:
        logger.info('')

    logger.info(f'[dim] ○  {escape(message)}[/dim]')  # noqa: G004


def print_success(message: str, pad_above: bool = False):
    """Print a message with a success indicator."""
    if pad_above:
        logger.info('')

    logger.info(f'{Symbols.CHECK_HEAVY} [bold]{escape(message)}[bold]')  # noqa: G004


def print_warning(message: str, pad_above: bool = False):
    """Print a message with a warning indicator."""
    if pad_above:
        logger.info('')

    logger.info(f'{Symbols.WARNING} {escape(message)}')  # noqa: G004


def print_fail(message: str, pad_above: bool = False):
    """Print a message with a failure indicator."""
    if pad_above:
        logger.info('')

    logger.error(
        f'{Symbols.CHECK_FAIL_EMOJI} [bold]{escape(message)}[/bold]',  # noqa: G004
    )


def list_to_string(parts: list, separator: str = ' ') -> str:
    """
    Combine list into string using a separator.

    Args:
        parts (list): required - List to combine.
        separator (str): optional - String to use as a separator, space (" ")
            is used by default.
    """
    parts = list(filter(lambda p: bool(p), parts))
    result_string = separator.join(parts)

    return result_string


def prompt_for_confirmation(message: str, exit_if_no: bool = True) -> bool:
    """
    Prompt the user for confirmation.

    Args:
        message (str): required - Message to display to the user.
        exit_if_no (bool): optional - Exit the program if the user does not

    Returns:
        bool: True if the user confirms, False otherwise.
    """
    # Acme modules
    from rich.prompt import Prompt

    confirmation = Prompt.ask(
        f'{message} [y/n]',
        choices=['y', 'n'],
    )

    proceed = confirmation == 'y'

    if exit_if_no and not proceed:
        logger.info('Exiting...')
        sys.exit(0)

    return proceed


class FluidRichHandler(logging.Handler):
    """Custom Rich Handler that turns off soft wrapping."""

    def emit(self, record):
        """Override the console options to print."""
        msg = self.format(record)
        Console(soft_wrap=True).print(msg)


# Use Rich for pretty logging in local terminal
logger = logging.getLogger('utils.formatting')
logger.setLevel(LOG_LEVEL)
formatter = logging.Formatter(LOG_FORMAT_STRING)
handler = FluidRichHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False
