from utils import setENV, verifyLinkedinURL, builder
from scraping import scraping
from pyfiglet import Figlet
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError



style = style_from_dict({
    Token.QuestionMark: '#ff2b73 bold',
    Token.Selected: '',
    Token.Instruction: '',
    Token.Answer: '#59dbff bold',
    Token.Question: '#f7b628 bold',
})


def welcome():
    f = Figlet(font='slant')
    print(f.renderText('ResuME'))

def init():
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
    obj = scraping(answers['Linkedin'])
    # function to build website and push website to github
    builder(obj)
    # function to deploy website to netlify
    # print('Pushed to github: xxx-xxx-xxx-xxx')
    # print('Deployed on netlify at link: xx-xxx-xx.netlify.app')
    print('Thanks!\nNext: Use the "websites" command')

def websites():
    print('all websites created are:\n')
    # function to fetch all websites from github
    print('Link: xxx.xxxxx.xxx')
