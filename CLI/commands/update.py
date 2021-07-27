import click
from utils import getENV, updateBuilder, verifyLinkedinURL
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
    """Updates an existing website using your linkedin profile"""
    questions = [
        {
            'type': 'input',
            'message': 'Enter Linkedin profile',
            'name': 'Linkedin'
        },
    ]
    answers = prompt(questions, style=style)
    verification = verifyLinkedinURL(answers["Linkedin"])
    if(verification ==None):
        print("Error: Linkedin link not valid");
        return;
    # scrap 
    github = getENV('owner')
    obj = scraping(answers['Linkedin'],github)
    op = updateBuilder(obj)
    if(op):
        print('Error: Repository doesn\'t exists! try the "build" command')
    else:
        print('Thanks!\nNext: Use the "websites" command')