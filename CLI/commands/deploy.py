import click
from utils import getENV, deployer
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
    """Deploy's your website to github pages, you need to use this command only once"""
    if(getENV("PAT")==None or getENV("username")==None or getENV("password")==None):
        print("please use 'init' command first");
        return;
    deploy()

def deploy():
    questions = [
        {
            'type': 'input',
            'message': 'Enter name of repository to be deployed',
            'name': 'repo'
        },
    ]
    ans = prompt(questions, style=style)
    repo = ans['repo']
    msg = deployer(repo)
    print(msg)
