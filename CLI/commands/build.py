import click
from utils import getENV, builder, verifyLinkedinURL
from scraping import scraping
from PyInquirer import style_from_dict, Token, prompt



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
    if(getENV("PAT")==None or getENV("username")==None or getENV("password")==None):
        print("please use 'init' command first");
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
            'message': 'Do you want to use a custom domain? (yes/no)',
            'name': 'domain'
        },
    ]

    answers = prompt(questions, style=style)

    if("y" in answers['domain'].lower()):
        dns_params = dns()
        print(answers)
        print(dns_params)
    
    verification = verifyLinkedinURL(answers["Linkedin"])
    if(verification ==None):
        print("Error: Linkedin link not valid");
        return;
    # Scrape
    github = getENV('owner')
    obj = scraping(answers['Linkedin'],github)
    # function to build website and push website to github
    op = builder(obj)
    if(op):
        print('Error: Repository already exists! try the "update" command')
    else:
        print('Thanks!\nNext: Use the "websites" command')


def dns():
    questions = [
        {
            'type': 'input',
            'message': 'Enter xxxx id:',
            'name': 'Domain_ID'
        },
        {
            'type': 'password',
            'message': 'Enter xxxx password:',
            'name': 'Domain_PASS'
        },
        {
            'type': 'input',
            'message': 'Enter xxxx domain name:',
            'name': 'Domain'
        }
    ]
    answers = prompt(questions, style=style)
    return answers
