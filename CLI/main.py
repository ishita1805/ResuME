import fire
from commands import init, build, websites, welcome
from utils import getENV

def initfunc():
    welcome()
    init()

def buildfunc():
    if(getENV("PAT")==None or getENV("username")==None or getENV("password")==None):
        print("please use 'init' command first");
        return;
    welcome()
    build()

def listfunc():
    welcome()
    websites()

if __name__ == '__main__':
    fire.Fire({
        'init': initfunc,
        'build': buildfunc,
        'list':listfunc
    })
