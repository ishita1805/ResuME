import click
import os
from colorama import Fore, init
import psutil

if psutil.Process(os.getpid()).parent().name() == 'cmd.exe':
    init(convert=True)

plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')

welcomstring = """\n
 _____                 __  __
|  _  \___  ___  _   _|  \/  | ___
| |_) / _ \/ __|| | | | |\/| |/ _ \\
|  _ <  __/\__ \| |_| | |  | |  __/
|_| \_\___||___/\__,__|_|  |_|\___|"""

def welcome():
    print(Fore.YELLOW+welcomstring.rstrip())
    print("\n")

class MyCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py') and filename != '__init__.py':
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(plugin_folder, name + '.py')
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns['cli']

cli = MyCLI(help=Fore.YELLOW+'This tool helps you generate beautiful websites in under 5 minuites. '+Fore.RED+'Requirement: Git CLI installed and authenticated on your device.'
            +Fore.LIGHTGREEN_EX+' Note: Please enter github details only for the account authenticated on your git CLI'+Fore.WHITE)


if __name__ == '__main__':
    welcome()
    cli()
