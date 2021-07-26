import fire
from commands import init, build, websites, welcome
from utils import getENV

def initfunc():
    init()

def buildfunc():
    if(getENV("PAT")==None or getENV("username")==None or getENV("password")==None):
        print("please use 'init' command first");
        return;
    build()

def listfunc():
    websites()

if __name__ == '__main__':
    welcome()
    fire.Fire({
        'init': initfunc,
        'build': buildfunc,
        'list':listfunc
    })
