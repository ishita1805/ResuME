import click
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
    """Deletes the specified website"""
    questions = [
        {
            'type': 'input',
            'message': 'Enter name of repository to be deleted',
            'name': 'repo'
        },
    ]
    ans = prompt(questions, style=style)
    repo = ans['repo']
    # delete this repo from output directory
    # delete this repo from github