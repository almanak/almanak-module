import click
from almanak.compression import compress, decompress


@click.group(name='alnamak')
def cli():
    '''
    Almanak CLI. Tools, services and workflows.
    '''
    pass


@click.command('compress', short_help='zip-compress file or folder')
# Optional dir and filename. Also overwrite, but I do not think it works.
@click.option('-d', '--target-dir', type=click.Path(writable=True, resolve_path=True),
    help='specify a different path to compress to')
@click.option('-n', '--target-name', type=click.STRING,
    help='specify a different name for the zip-file. Leave out the zip-extension')
@click.option('-o', '--overwrite', is_flag=True, help='overwrite any existing file')
@click.argument('path', type=click.Path(exists=True, resolve_path=True))
def compress_cmd(path, target_dir, target_name, overwrite):
    """
    Saves a zip-compressed copy of <PATH> in the same directory.
    
    TARGET 
    OVERWRITE forces overwrite of any existing file with same filename.
    """
    zip_path = compress(path, target=target_dir, name=target_name, overwrite=overwrite)
    click.echo('INFO: zip-file created: ' + str(zip_path))


@click.command('decompress', short_help='decompress a zipfile')
# Optional extract-directory. Also overwrite, but does probably not work.
@click.option('-d', '--target-dir', type=click.Path(writable=True, resolve_path=True),
    help='specify a different path to extract to')
@click.option('-o', '--overwrite', is_flag=True,
    help='overwrite any existing file or directory')
@click.argument('path', type=click.Path(exists=True, resolve_path=True))
def decompress_cmd(path, target_dir, overwrite):
    """
    Decompresses a zipfile PATH into its parent-directory or TARGET.
    Use OVERWRITE to overwrite any existing file or directory with same name.
    """
    click.echo('path: ' + str(path))
    click.echo('target: ' + str(target_dir))
    click.echo('overwrite: ' + str(overwrite))


@click.command('clear', short_help='clear the screen')
def clear_cmd():
    """Clears the visible screen in a platform-agnostic way"""
    click.clear()

cli.add_command(compress_cmd)
cli.add_command(decompress_cmd)
cli.add_command(clear_cmd)


if __name__ == '__main__':
    cli()
