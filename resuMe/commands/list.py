import click
from colorama import Fore, init

from utils import list
# from resuMe.utils import list


@click.command()
def cli():
    """Lists all generated website locations"""
    try:
        list()
    except Exception as e:
        print(Fore.RED+"An error occured please try again"+Fore.WHITE)
        pass
    