import click
from PyInquirer import style_from_dict, Token, prompt
import os
from colorama import Fore, init
import psutil

from utils import getENV, updateBuilder, verifyLinkedinURL
from scraping import scraping

# from resuMe.utils import getENV, updateBuilder, verifyLinkedinURL
# from resuMe.scraping import scraping

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
    try:
        if(getENV("PAT")==None or getENV("owner")==None):
            print(Fore.RED+"Error: please use the command: `resuMe init` first"+Fore.WHITE);
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
            print(Fore.RED+"Error: Linkedin URL not valid"+Fore.WHITE)
            return;
        # scrap 
        obj = scraping(answers['Linkedin'],answers['Github'])
        op = updateBuilder(obj)
        if(op):
            print(Fore.RED+'Error: Repository doesn\'t exists! try the command: `resuMe build`'+Fore.WHITE)
        else:
            print(Fore.LIGHTGREEN_EX+'Yay! your website is updated\nNext: Use the command: `resuMe list`'+Fore.WHITE)
    except Exception as e:
        print(Fore.RED+"An error occured please try again"+Fore.WHITE)
        pass