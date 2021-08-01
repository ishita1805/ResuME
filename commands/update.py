import click
from utils import getENV, updateBuilder, verifyLinkedinURL
from scraping import scraping
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
    """Updates an existing website using your linkedin profile"""
    if(getENV("PAT")==None or getENV("owner")==None):
        print(Fore.RED+"Error: please use 'init' command first");
        return;
    questions = [
        {
            'type': 'input',
            'message': 'Enter Linkedin profile',
            'name': 'Linkedin'
        },
        {
            'type': 'input',
            'message': 'Enter Github username',
            'name': 'Github'
        },
    ]
    answers = prompt(questions, style=style)
    verification = verifyLinkedinURL(answers["Linkedin"])
    if(verification ==None):
        print(Fore.RED+"Error: Linkedin link not valid")
        return;
    # scrap 
    obj = scraping(answers['Linkedin'],answers['Github'])
    op = updateBuilder(obj)
    if(op):
        print(Fore.RED+'Error: Repository doesn\'t exists! try the "build" command')
    else:
        print(Fore.LIGHTGREEN_EX+'Thanks!\nNext: Use the "websites" command')