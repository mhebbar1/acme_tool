"""
Main entry point module for the acme-cli tool.

Run this file with the python3 command to start the cli.
"""
import click # type: ignore

from acme.commands.delete import delete
from acme.commands.deploy import deploy
from acme.commands.logs import logs
from acme.commands.ls import ls


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option()
def root():
    """
    Welcome to the Acme CLI
    \f
    This defines the main click group as the entry point to the CLI.
    """


# root commands
root.add_command(deploy)
root.add_command(delete)
root.add_command(logs)
root.add_command(ls)

if __name__ == '__main__':
    root()
