import click

@click.group(name='alnamak')
def cli():
    '''Almanak CLI. Tools, services and workflows.'''
    pass

@click.command('compress', short_help='init the repo')
@click.option('--target', type=click.Path(writable=True, resolve_path=True),
            help='')
@click.option('--overwrite', is_flag=True)
@click.argument('path', type=click.Path(exists=True, resolve_path=True))
def compress(path, target, overwrite):
    """Generates a Zip64-compressed copy of PATH into parent-directory or TARGET"""
    click.echo('path: ' + path)

@click.command()
def clear():
    """Clears the visible screen in a platform-agnostic way"""
    click.clear()

cli.add_command(compress)
cli.add_command(clear)


if __name__ == '__main__':
    cli()
