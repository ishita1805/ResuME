import click
import os
from colorama import Fore

@click.command()

def cli():
    """Lists all generated website locations"""
    output_path = os.path.join(os.path.dirname(__file__), 'Output')
    os.chdir(output_path)
    # os.system('dir')
    list = os.listdir(path='.')
    if(len(list)== 1):
        print(Fore.GREEN+'No ResuMe\'s Available, Try the "build" command'+Fore.WHITE)
    else:
        print(Fore.GREEN+'Available ResuMe\'s:')
        for i in range(1,len(list)):
            print(Fore.GREEN+list[i])
        print(''+Fore.WHITE)