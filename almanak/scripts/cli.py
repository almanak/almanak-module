import click
from almanak.compression import compress, decompress


@click.group(name='alnamak')
def cli():
    '''
    Almanak CLI. Tools, services and workflows.
    '''
    pass


@click.command('compress', short_help='zip-compress file or folder')
@click.option('--target-dir', type=click.Path(writable=True, resolve_path=True),
    help='specify a different path to compress to')
@click.option('--target-name', type=click.Path(writable=True, resolve_path=True),
    help='specify a different path to compress to')
@click.option('--overwrite', is_flag=True, help='overwrite any existing file')
@click.argument('path', type=click.Path(exists=True, resolve_path=True))
def compress_cmd(path, target, overwrite):
    """
    Saves a zip-compressed copy of <PATH> in the same directory.
    
    TARGET 
    OVERWRITE forces overwrite of any existing file with same filename.
    """
    click.echo('path: ' + str(path))
    click.echo('overwrite: ' + str(overwrite))


@click.command('decompress', short_help='decompress zipfile')
@click.option('--target', type=click.Path(writable=True, resolve_path=True),
    help='specify a different path to extract to')
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


@click.command('clear', short_help='clear the screen')
def clear_cmd():
    """Clears the visible screen in a platform-agnostic way"""
    click.clear()

cli.add_command(compress_cmd)
cli.add_command(decompress_cmd)
cli.add_command(clear_cmd)


if __name__ == '__main__':
    cli()
