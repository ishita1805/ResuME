import os
import json
import re

def setENV(envs):
    os.environ["username"] = str(envs["username"])
    os.environ["password"] = str(envs["password"])

def getENV(name):
    return os.getenv(name)

def verifyLinkedinURL(url):
    link = re.compile('((http(s?)://)*([www])*\.|[linkedin])[linkedin/~\-]+\.[a-zA-Z0-9/~\-_,&=\?\.;]+[^\.,\s<]')
    return(link.match(url))

def builder(data):
    # api request
    print('website builder')

def netlify(data):
    # api request
    print('deploy to netlify')

