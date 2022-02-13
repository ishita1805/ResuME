import click
from PyInquirer import style_from_dict, Token, prompt
import os
from colorama import Fore, init
import psutil

if os.getenv('DEV') == 'True':
    from utils import setENV
else:
    from resuMe.utils import setENV

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
    try:
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
            {
                'type': 'input',
                'message': 'Enter your linkedin email',
                'name': 'Email'
            },
            {
                'type': 'input',
                'message': 'Enter your linkedin password (don\'t worry, it is stored only on your local machine)',
                'name': 'Password'
            },
            {
                'type': 'input',
                'message': 'Where do you want to store your resuMe\'s? (enter an absolute path to the directory)',
                'name': 'Output'
            },
        ]
        answers = prompt(questions, style=style)
        setENV(answers)
        print(Fore.LIGHTGREEN_EX+'Yay! you are all set up\nNext: Use the command: `resume-cli build`'+Fore.WHITE);
    except Exception as e:
        print(Fore.RED+"An error occured please try again"+Fore.WHITE)
        pass