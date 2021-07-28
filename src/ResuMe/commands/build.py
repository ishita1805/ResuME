import click
from utils import getENV, builder, verifyLinkedinURL, welcome
from scraping import scraping
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
    """Generates a new website using your linkedin profile"""
    welcome()
    if(getENV("PAT")==None or getENV("owner")==None):
        print(Fore.RED+"Error: Please use 'init' command first"+Fore.WHITE);
        return;
    build()


def build():
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
        print(Fore.RED+"Error: Linkedin link not valid"+Fore.WHITE);
        return;
    # Scrape
    obj = scraping(answers['Linkedin'],answers['Github'])
    # function to build website and push website to github
    op = builder(obj)
    if(op):
        print(Fore.RED+'Error: Repository already exists! try the "update" command'+Fore.WHITE)
    else:
        print(Fore.GREEN+'Thanks!\nNext: Use the "deploy" command'+Fore.WHITE)

