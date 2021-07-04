from utils import setENV, verifyLinkedinURL
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
    f = Figlet(font='')
    print(f.renderText('ResuME'))


def init():
    questions = [
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


def build():
    questions = [
        {
            'type': 'input',
            'message': 'Enter Linkedin profile',
            'name': 'Linkedin'
        },
        {
            'type': 'input',
            'message': 'Do you want to use a custom domain? (Leave blank if "No")',
            'name': 'domain'
        },
    ]

    answers = prompt(questions, style=style)
    if(answers['domain']):
        dns_params = dns()
        print(answers)
        print(dns_params)
    # print(answers)
    # print('\n')   
    verification = verifyLinkedinURL(answers["Linkedin"])
    if(verification == 'None'):
        print("Error: Linkedin link not valid")
    else:
        # function to scrape and handle error
        # function to build website and push website to github
        # function to deploy website to netlify
        print('Deployed to github at link: xxx-xxx-xxx-xxx')
        print('Deployed on netlify at link: xx-xxx-xx.netlify.app')
        print('Thanks!\nNext: Use the "dns" command')


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


def websites():
    print('all websites deployed are:\n')
    # function to fetch all websites
    print('URL: xxx.xxxxx.xxx')
