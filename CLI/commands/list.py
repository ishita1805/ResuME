import click
import os
from colorama import Fore

@click.command()

def cli():
    """Lists all generated website locations"""
    os.chdir(r"../Output")
    # os.system('dir')
    list = os.listdir(path='.')
    if(len(list)== 1):
        print(Fore.GREEN+'No ResuMe\'s Available')
    else:
        print(Fore.GREEN+'Available ResuMe\'s:')
        for i in range(len(list)):
            print(Fore.GREEN+list[i])
    