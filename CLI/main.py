import fire
from commands import init, build, websites

def initfunc():
    init()

def buildfunc():
    # function to check if env variables are set
    build()

def listfunc():
    websites()

if __name__ == '__main__':
    fire.Fire({
        'init': initfunc,
        'build': buildfunc,
        'list':listfunc
    })

#  COMMANDS 
# 1. resume Init
# - enter github dev key and save it to system variables
# - enter netlify id and pass and save it to system variables

# 2. resume build
# - enter linkedin profile and generate a zip
# - deploy it to netlify
# - display netlify link to user

#4. LIST
#- list all domains in use from netlify

# TO-Do list
# 1. Write bash script for installation
# 2. Fix bug in the scraping script
# 3. Create a requirements.txt file