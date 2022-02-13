import click
import os
from colorama import Fore, init

if os.getenv('DEV') == 'True':
    from utils import list
else:
    from resuMe.utils import list


@click.command()
def cli():
    """Lists all generated website locations"""
    try:
        list()
    except Exception as e:
        print(Fore.RED+"An error occured please try again"+Fore.WHITE)
        pass
    