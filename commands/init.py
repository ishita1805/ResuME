import click
from utils import setENV
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
    """Sets up your credentials"""
    questions = [
        {
            'type': 'input',
            'message': 'Enter your github username',
            'name': 'owner'
        },
        {
            'type': 'input',
            'message': 'Enter your github PAT',
            'name': 'PAT'
        },
    ]
    answers = prompt(questions, style=style)
    setENV(answers)
    print(Fore.LIGHTGREEN_EX+'Thanks! \nNext: Use the "build" command');