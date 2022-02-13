import click
from PyInquirer import style_from_dict, Token, prompt
import os
from colorama import Fore, init
import psutil

if os.getenv('DEV') == 'True':
    from utils import delRepo, getENV
else:
    from resuMe.utils import delRepo, getENV

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
    """Deletes the specified website"""
    try:
        if(getENV("PAT")==None or getENV("owner")==None):
            print(Fore.RED+"Error: please use the command: `resume-cli init` first"+Fore.WHITE)
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
    except Exception as e:
        print(Fore.RED+"An error occured please try again"+Fore.WHITE)
        pass
    

   