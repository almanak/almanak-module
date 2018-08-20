import click
from almanak.compression import compress, decompress

@click.group(name='alnamak')
def cli():
    '''
    Almanak CLI. Tools, services and workflows.
    '''
    pass


@click.command('compress', short_help='zip-compress file or folder')
@click.option('--target', type=click.Path(writable=True, resolve_path=True),
    help='specify alternate output-filepath')
@click.option('--overwrite', is_flag=True, help='overwrite any existing file')
@click.argument('path', type=click.Path(exists=True, resolve_path=True))
def compress_cmd(path, target, overwrite):
    """
    Saves a Zip64-compressed copy of PATH in its parent-directory or TARGET.
    Use OVERWRITE to overwrite any existing file with same filename.
    """
    click.echo('path: ' + path)
    click.echo('target: ' + target)
    click.echo('overwrite: ' + overwrite)


@click.command('decompress', short_help='decompress zipfile')
@click.option('--target', type=click.Path(writable=True, resolve_path=True),
    help='specify alternate output-filepath')
@click.option('--overwrite', is_flag=True,
    help='overwrite any existing file or directory')
@click.argument('path', type=click.Path(exists=True, resolve_path=True))
def decompress_cmd(path, target, overwrite):
    """
    Decompresses a zipfile PATH into its parent-directory or TARGET.
    Use OVERWRITE to overwrite any existing file or directory with same name.
    """
    click.echo('path: ' + path)
    click.echo('target: ' + target)
    click.echo('overwrite: ' + overwrite)


@click.command('help', short_help='show this help-message and exit')
def help():
    """Clears the visible screen in a platform-agnostic way"""
    click.clear()

cli.add_command(compress)
cli.add_command(help)


if __name__ == '__main__':
    cli()
