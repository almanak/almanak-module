import click
from almanak.file import file_cli as _file


@click.group(name='almanak')
def cli():
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
