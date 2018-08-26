import click
import logging

from .file import compress, decompress, extract, fileinfo

logger = logging.getLogger(__name__)

@click.group(name='file')
def file_cli():
    '''
    Operations on a single file or directory (zip)
    '''
    pass


@click.command('info', short_help='info on a file or zip-archive')
@click.argument('path', type=click.Path(exists=True, resolve_path=True))
def info_cmd(path):
    '''
    Get information on a file (incl. zip-archives)
    '''
    # click.echo_via_pager('\n'.join('Line %d' % idx
    #                                for idx in range(200)))
    try:
        click.echo(fileinfo(path))
    except Exception as e:
        logger.error("something went wrong")
        logger.exception(e)

@click.command('extract', short_help='extract file from zip-archive')
@click.argument('file', type=click.Path())
@click.argument('archive', type=click.Path(exists=True))
@click.option('--target-dir',
              type=click.Path(writable=True, resolve_path=True),
              help='specify a different directory to extract to')
@click.option('--overwrite', is_flag=True,
              help='overwrite any existing file or directory')
def extract_cmd(file, archive, target_dir, overwrite):
    '''
    Extracts a <file> from a <archive> (zip-formatted).
    '''
    try:
        out_path = extract(file_path=file, zip_path=archive,
                           out_path=target_dir, overwrite=overwrite)
        ctx = click.get_current_context()
        for k, v in ctx.params.items():
            click.echo("ctx-key: " + str(k) + ", ctx-value: " + str(v))
        click.echo(type(ctx.params))
        # if click.get_current_context().verbose:
        #     click.echo('INFO: zip-member extracted to: ' + out_path)
        # else:
        #     click.echo('This is not printet to stout, as verbose is not set')
    except Exception:
        logger.exception('unable to extact file from zip-archive')
        raise


@click.command('compress', short_help='zip-compress file or directory')
# Optional dir and filename. Also overwrite, but I do not think it works.
@click.option('--target-dir',
              type=click.Path(writable=True, resolve_path=True),
              help='specify a different directory to compress to')
@click.option('--target-name', type=click.STRING,
              help='specify a new name for the zip-file.')
@click.option('--overwrite', is_flag=True, help='overwrite any existing file')
@click.argument('path', type=click.Path(exists=True, resolve_path=True))
def compress_cmd(path, target_dir, target_name, overwrite):
    """
    Saves a zip-compressed copy of <PATH> in the same directory.
    """
    try:
        zip_path = compress(path, target=target_dir, name=target_name,
                            overwrite=overwrite)
        if click.get_current_context().verbose is True:
            click.echo('INFO: zip-file created: ' + zip_path)
        else:
            click.echo('This is not printet to stout, as verbose is not set')
    except Exception as e:
        click.echo('Error: ' + str(e))


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


file_cli.add_command(extract_cmd)
file_cli.add_command(compress_cmd)
file_cli.add_command(decompress_cmd)
# file_cli.add_command(validate_cmd)
# file_cli.add_command(identify_mcd)
# file_cli.add_command(hash_cmd)
file_cli.add_command(info_cmd)
