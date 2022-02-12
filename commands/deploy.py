import click
from utils import getENV, deployer
from PyInquirer import style_from_dict, Token, prompt
import os
from colorama import Fore, init
import psutil

if psutil.Process(os.getpid()).parent().name() == 'cmd.exe':
    init(convert=True)
    
style = style_from_dict({
    Token.QuestionMark: '#ff2b73 bold',
    Token.Selected: '',
    Token.Instruction: '',
    Token.Answer: '#59dbff bold',
    Token.Question: '#f7b628 bold',
})


@click.command()
def cli():
    """Deploys website to github pages, auto deploys on updates"""
    if(getENV("PAT")==None or getENV("owner")==None):
        print(Fore.RED+"Error: please use the command: `resuMe init` first"+Fore.WHITE)
        return;
    deploy()

def deploy():
    questions = [
        {
            'type': 'input',
            'message': 'Name of the github repository to be deployed',
            'name': 'repo'
        },
    ]
    ans = prompt(questions, style=style)
    repo = ans['repo']
    msg = deployer(repo)
    print(Fore.LIGHTGREEN_EX+'Your ResuMe is deployed at: '+msg+Fore.WHITE)
