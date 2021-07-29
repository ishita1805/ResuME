import click
import os
from colorama import Fore
from pyfiglet import Figlet

plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')


def welcome():
    f = Figlet(font='slant')
    print(f.renderText('ResuME'))

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

cli = MyCLI(help=Fore.GREEN+'This tool helps you generate beautiful websites in under 5 minuites. '+Fore.LIGHTRED_EX+'Requirement: Git CLI installed and authenticated on your device.'
            +Fore.CYAN+' Note: Please enter github details only for the account authenticated on your git CLI'+Fore.WHITE)


if __name__ == '__main__':
    welcome()
    cli()
