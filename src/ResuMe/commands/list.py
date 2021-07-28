import click
import os
from colorama import Fore
from utils import welcome

@click.command()

def cli():
    """Lists all generated website locations"""
    welcome()
    os.chdir(r"../Output")
    # os.system('dir')
    list = os.listdir(path='.')
    if(len(list)== 1):
        print(Fore.GREEN+'No ResuMe\'s Available')
    else:
        print(Fore.GREEN+'Available ResuMe\'s:')
        for i in range(1,len(list)):
            print(Fore.GREEN+list[i])
        print(Fore.WHITE+'')