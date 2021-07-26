import fire
from commands import init, build, websites, welcome, update
from utils import getENV


def buildfunc():
    if(getENV("PAT")==None or getENV("username")==None or getENV("password")==None):
        print("please use 'init' command first");
        return;
    build()



if __name__ == '__main__':
    welcome()
    fire.Fire({
        'init': init,
        'build': buildfunc,
        'list':websites,
        'update':update
    })
