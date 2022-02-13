import click
from PyInquirer import style_from_dict, Token, prompt
import os
from colorama import Fore, init
import psutil

if os.getenv('DEV') == 'True':
    from utils import getENV, updateBuilder, verifyLinkedinURL
    from scraping import scraping
else:
    from resuMe.utils import getENV, updateBuilder, verifyLinkedinURL
    from resuMe.scraping import scraping

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
            print(Fore.RED+"Error: please use the command: `resume-cli init` first"+Fore.WHITE);
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
            {
            'type': 'checkbox',
            'message': 'Select a theme (default purple)',
            'name': 'Theme',
            'choices': [ 
                {
                    'name': 'blue'
                },
                {
                    'name': 'purple'
                },
                {
                    'name': 'orange'
                }
            ]
        },
        ]
        answers = prompt(questions, style=style)
        # verifying theme
        if len(answers["Theme"]) == 0 :
            print(Fore.RED+"Error: Please select atleast one theme"+Fore.WHITE);
            return;
        if len(answers["Theme"]) > 1 :
            print(Fore.RED+"Error: Please select only one theme"+Fore.WHITE);
            return;
        verification = verifyLinkedinURL(answers["Linkedin"])
        if(verification ==None):
            print(Fore.RED+"Error: Linkedin URL not valid"+Fore.WHITE)
            return;
        # get creds
        email = getENV("Email");
        password = getENV("Password");
        # scrap 
        obj = scraping(
            email,
            password,
            answers['Linkedin'],
            answers['Github'],
            answers['Theme'][0]
        )
        op = updateBuilder(obj)
        if(op):
            print(Fore.RED+'Error: Repository doesn\'t exists! try the command: `resume-cli build`'+Fore.WHITE)
        else:
            print(Fore.LIGHTGREEN_EX+'Yay! your website is updated\nNext: Use the command: `resume-cli list`'+Fore.WHITE)
    except Exception as e:
        print(Fore.RED+"An error occured please try again"+Fore.WHITE)
        pass