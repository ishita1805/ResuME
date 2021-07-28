import os
import re
import json
import sys
import requests
import shutil


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

    configDir = os.path.join(os.path.join(app_config_dir, ".localconfig"), 'configstore')
    # print(configDir)

    createPath(configDir)
    if os.path.exists(configDir) and not os.path.isfile(os.path.join(configDir, 'ResuME.json')):
        with open(os.path.join(configDir, 'ResuME.json'), 'w') as cf:
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


def builder(data):
    dta = json.loads(data)
    # check if folder exists in the Output directory or github repo
    dest = "../Output/ResuMe-"+dta['profile']['Name'].replace(" ","-")
    if(os.path.isdir(dest)):
        return True;
    # add data.json to template folder 
    with open("../Template/data.json", "w") as outfile:
        outfile.write(data)
    github(dta['profile']['Name'])


def github(name):
    src = "../Template/"
    dest = "../Output/ResuMe-"+name.replace(" ","-")
    PAT = getENV("PAT")
    Owner = getENV("owner")
    API_URL = 'https://api.github.com'
    Payload = '{ "name":"ResuMe-'+name.replace(" ","-")+'", "description":"This repository is auto generated by ResuME-Website Generator" }'
    Headers = {
        "Authorization": "token "+PAT,
        "Accept": "application/vnd.github.v3+json"
    }
    # create a new repo
    requests.post(API_URL+'/user/repos',data=Payload, headers=Headers)
    # copy template folder files into output folder
    shutil.copytree(src, dest)
    # push to github
    os.chdir(r"../Output/ResuMe-"+name.replace(" ","-"))
    os.system("git init")
    os.system("git add .")
    os.system("git commit -m 'website-generated'")
    os.system("git remote add origin https://github.com/"+Owner+"/ResuMe-"+name.replace(" ","-")+".git")
    os.system("git push origin master -f")
    

def updateBuilder(data):
    dta = json.loads(data)
    # check if folder doesn't exists
    dest = "../Output/ResuMe-"+dta['profile']['Name'].replace(" ","-")
    if(os.path.isdir(dest)==False):
        return True;
    # add data.json to output folder 
    with open("../Output/ResuMe-"+dta['profile']['Name'].replace(" ","-")+"/data.json", "w") as outfile:
        outfile.write(data)
    # push to github
    os.chdir(r"../Output/ResuMe-"+dta['profile']['Name'].replace(" ","-"))
    os.system("git add .")
    os.system("git commit -m 'website-updated'")
    os.system("git push origin master -f")


def deployer(repo):
    # change directory and create a new branch
    os.chdir(r"../Output/"+repo)
    os.system('git checkout -b gh-pages')
    
    # modify readme file
    f = open('README.md','a')
    f.write('\n**your ResuMe is deployed at:** https://'+getENV('owner')+'.github.io/'+repo+'\n')
    f.close()
    # push new branch to github
    os.system("git add .")
    os.system("git commit -m 'website-deployed'")
    os.system("git push origin gh-pages")

    return 'https://'+getENV('owner')+'.github.io/'+repo+'/'





