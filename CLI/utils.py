import os
import re
import json
import sys

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
    # node wrapper to create a json file using obj in the template folder and then upload the template folder to github
    # api request to push the website to github
    # api request to deploy github link to netlify
    print(data)

def netlify(data):
    # api request
    print('deploy to netlify')

