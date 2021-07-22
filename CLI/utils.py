import os
import re
import json
import sys
import requests

def createPath(path):
    if not os.path.exists(path):
        os.makedirs(path, 777)
        return True

def getConfigDir():
    if sys.platform == "win32":
        app_config_dir = os.getenv("LOCALAPPDATA")
    else:
        app_config_dir = os.getenv("HOME")
        if os.getenv("XDG_CONFIG_HOME"):
            app_config_dir = os.getenv("XDG_CONFIG_HOME")

    configDir = os.path.join(os.path.join(
        app_config_dir, ".localconfig"), 'configstore')

    createPath(configDir)
    if os.path.exists(configDir) and not os.path.isfile(os.path.join(configDir, 'QuiCLI.json')):
        with open(os.path.join(configDir, 'QuiCLI.json'), 'w') as cf:
            json.dump({}, cf)
    return configDir

def setENV(envs):
   with open(os.path.join(getConfigDir(), 'ResuME.json'), 'w') as f:
        json.dump(envs, f)

def getENV(item):
    with open(os.path.join(getConfigDir(), 'ResuME.json')) as f:
        data = json.load(f)
    return data[item]

def verifyLinkedinURL(url):
    link = re.compile('((http(s?)://)*([www])*\.|[linkedin])[linkedin/~\-]+\.[a-zA-Z0-9/~\-_,&=\?\.;]+[^\.,\s<]')
    return(link.match(url))

# TODO

def builder(data):
    with open("../Template/data.json", "w") as outfile:
        outfile.write(data)
    github()
    # api request to push the website to github
    # api request to deploy github link to netlify

def netlify(data):
    # api request
    print('deploy to netlify')

def github():
    # variables
    PAT = getENV("PAT")
    API_URL = 'https://api.github.com'
    Owner = getENV("owner")
    Payload = '{ "name":"My-ResuME-Website" }'
    Headers = {
        "Authorization": "token "+PAT,
        "Accept": "application/vnd.github.v3+json"
    }
    # create a new repo
    requests.post(API_URL+'/user/repos',data=Payload, headers=Headers)
    # push the template folder to the repo
    push_to_github(Owner,"My-ResuME-Website","data.json",'"{"message":"dummy json data"}"')

def push_to_github(owner, repo, path, data):
    PAT = getENV("PAT")
    API_URL = 'https://api.github.com'
