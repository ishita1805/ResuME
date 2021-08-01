import click
from utils import delRepo, getENV
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
    """Deletes the specified website"""
    if(getENV("PAT")==None or getENV("owner")==None):
        print(Fore.RED+"Error: please use 'init' command first"+Fore.WHITE);
        return;
    questions = [
        {
            'type': 'input',
            'message': 'Enter name of repository to be deleted',
            'name': 'repo'
        },
    ]
    ans = prompt(questions, style=style)
    delRepo(ans['repo'])
    

   