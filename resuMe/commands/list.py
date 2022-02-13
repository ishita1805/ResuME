import click

from utils import list
# from resuMe.utils import list


@click.command()
def cli():
    """Lists all generated website locations"""
    list()
    