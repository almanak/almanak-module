import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('hello %s!' % name)

@click.command()
def clear():
    """Clears the visible screen in a platform-agnostic way"""
    click.clear()


if __name__ == '__main__':
    hello()
