import click
from utils import setENV
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
    """Sets up the CLI with your credentials"""
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
            'message': 'Enter your netlify API Token',
            'name': 'username'
        },
        {
            'type': 'password',
            'message': 'Enter your netlify API Secret',
            'name': 'password'
        },
        
    ]
    answers = prompt(questions, style=style)
    setENV(answers)
    print('Thanks! \nNext: Use the "build" command')