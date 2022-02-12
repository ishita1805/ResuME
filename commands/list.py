import click
from utils import list

@click.command()
def cli():
    """Lists all generated website locations"""
    list()
    