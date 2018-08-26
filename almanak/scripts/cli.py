# Standard library
import logging
# from pathlib import Path
from os import path

# Third party
import click

# Application
from almanak.file import file_cli as file_commands


# Setup for CLI-logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# info and higher to stderr-handler (default stream for Streamhandler)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(levelname)s \t %(message)s")
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)
# all to logfile
file_handler = logging.FileHandler(path.expanduser('~/.almanak_log.txt'))
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter("%(asctime)s %(levelname)s \t %(funcname)s %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


@click.option('--verbose', is_flag=True, default=False,
              help='ouput all log-levels to strout')
@click.group(name='almanak')
def cli(verbose=False):
    '''
    Almanak CLI. Tools, services and workflows for almanak-repos.
    '''
    logger.info("cli_cmd called")
    click.echo(logger.name)
    pass


cli.add_command(file_commands.file_cli)
# cli.add_command(file_commands.compress_cmd)
# cli.add_command(file_commands.decompress_cmd)

if __name__ == '__main__':
    cli()
