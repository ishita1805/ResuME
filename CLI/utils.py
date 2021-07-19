import os
import re
import json
# working
def setENV(envs):
    os.environ["username"] = str(envs["username"])
    os.environ["password"] = str(envs["password"])
    os.environ["PAT"] = str(envs["PAT"])
# working
def getENV(name):
    return os.getenv(name)
# working
def verifyLinkedinURL(url):
    link = re.compile('((http(s?)://)*([www])*\.|[linkedin])[linkedin/~\-]+\.[a-zA-Z0-9/~\-_,&=\?\.;]+[^\.,\s<]')
    return(link.match(url))

def builder(data):
    obj = json.dumps(data, indent = 4)
    # node wrapper to create a json file using obj in the template folder and then upload the template folder to github
    # api request to push the website to github
    print(obj)

def netlify(data):
    # api request
    print('deploy to netlify')

