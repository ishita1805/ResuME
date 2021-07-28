import click
import requests
import shutil
import os
from utils import getENV, welcome
from PyInquirer import style_from_dict, Token, prompt
from colorama import Fore
import stat
from os import path


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
    welcome()
    if(getENV("PAT")==None or getENV("username")==None or getENV("password")==None):
        print(Fore.RED+"Error: please use 'init' command first"+Fore.WHITE);
        return;
    questions = [
        {
            'type': 'input',
            'message': 'Enter name of repository to be deleted',
            'name': 'repo'
        },
    ]
    ans = prompt(questions, style=style)
    repo = ans['repo']
    os.chdir(r"../Output")
    check = False
    # check if repo exists
    list = os.listdir(path='.')
    for i in range(1,len(list)):
        if(list[i] == repo):
            check = True
    if(check == False):
        print(Fore.RED+'Error: ResuMe not found'+Fore.WHITE)
        return;
    # delete this repo from output directory
    for root, dirs, files in os.walk(repo):  
        for dir in dirs:
            os.chmod(path.join(root, dir), stat.S_IRWXU)
        for file in files:
            os.chmod(path.join(root, file), stat.S_IRWXU)
    shutil.rmtree(repo)
    
    # delete this repo from github
    PAT = getENV("PAT")
    Owner = getENV("owner")
    API_URL = 'https://api.github.com/repos/'+Owner+'/'+repo
    Headers = {
        "Authorization": "token "+PAT,
        "Accept": "application/vnd.github.v3+json"
    }
    requests.delete(API_URL, headers=Headers)

   

    print(Fore.GREEN+'\nResuMe Deleted'+Fore.WHITE)

   