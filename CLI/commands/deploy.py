import click
from utils import getENV, deployer
from PyInquirer import style_from_dict, Token, prompt
from colorama import Fore

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
    if(getENV("PAT")==None or getENV("username")==None or getENV("password")==None):
        print("please use 'init' command first");
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
    print(Fore.GREEN+'Your ResuMe is deployed at: '+msg)
