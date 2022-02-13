import sys
import subprocess
from colorama import Fore
import os
import shutil

# list of packages
packages = [
    'click==7.1.2',
    'PyInquirer==1.0.3',
    'selenium== 3.141.0',
    'bs4==0.0.1',
    'requests==2.26.0',
    'lxml==4.6.3',
    'webdriver-manager==3.4.1',
    'colorama==0.4.4',
    'psutil==5.8.0',
    'setuptools',
    'wheel',
    'python-dotenv'
]

# implement pip as a subprocess:
for package in packages:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# process output with an API in the subprocess module:
reqs = subprocess.check_output([sys.executable, '-m', 'pip',
'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

# copy .env.example to .env in resuMe
path = os.getcwd()
shutil.copyfile(path+'/resuMe/.env.example',path+'/resuMe/.env');

print(Fore.LIGHTGREEN_EX+'Yay! ResuMe is all set up\n'+Fore.WHITE)