import click
from almanak.file import file_cli as _file

@click.option('--verbose', is_flag=True, default=False,
              help='ouput all log-levels to strout')
@click.group(name='almanak')
def cli(verbose=False):
    '''
    Almanak CLI. Tools, services and workflows for almanak-repos.
    '''
    pass


# cli.add_command(_file.compress_cmd)
# cli.add_command(_file.decompress_cmd)
cli.add_command(_file.file_cli)
# 

if __name__ == '__main__':
    cli()
