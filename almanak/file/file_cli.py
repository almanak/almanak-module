import click
from .file import compress, decompress


@click.group(name='file')
def file_cli():
    pass


@click.command('compress', short_help='zip-compress file or folder')
# Optional dir and filename. Also overwrite, but I do not think it works.
@click.option('--target-dir', type=click.Path(writable=True, resolve_path=True),
    help='specify a different directory to compress to')
@click.option('--target-name', type=click.STRING,
    help='specify a new name for the zip-file. Leave out the ".zip"-extension')
@click.option('--overwrite', is_flag=True, help='overwrite any existing file')
@click.argument('path', type=click.Path(exists=True, resolve_path=True))
def compress_cmd(path, target_dir, target_name, overwrite):
    """
    Saves a zip-compressed copy of <PATH> in the same directory.
    """
    zip_path = compress(path, target=target_dir, name=target_name, overwrite=overwrite)
    click.echo('INFO: zip-file created: ' + str(zip_path))


@click.command('decompress', short_help='decompress a zipfile')
# Optional extract-directory. Also overwrite, but does probably not work.
@click.option('--target-dir', type=click.Path(writable=True, resolve_path=True),
    help='specify a different path to extract to')
@click.option('--overwrite', is_flag=True,
    help='overwrite any existing files or directories')
@click.argument('path', type=click.Path(exists=True, resolve_path=True))
def decompress_cmd(path, target_dir, overwrite):
    """
    Decompresses a zipfile PATH into its parent-directory or TARGET.
    Use OVERWRITE to overwrite any existing file or directory with same name.
    """
    click.echo('path: ' + str(path))
    click.echo('target: ' + str(target_dir))
    click.echo('overwrite: ' + str(overwrite))


file_cli.add_command(compress_cmd)
file_cli.add_command(decompress_cmd)