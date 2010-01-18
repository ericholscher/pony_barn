import sys
from pony_barn import client as pony
from base import BaseBuild

class PonyBuild(BaseBuild):

    def __init__(self):
        super(PonyBuild, self).__init__()
        self.name = "sphinx"
        self.required = ['nose']
        self.repo_url = 'http://bitbucket.org/birkenfeld/sphinx/'

    def define_commands(self):
        self.commands = [
            pony.HgClone(self.repo_url, egg=self.get_name()),
            pony.BuildCommand([self.context.python, 'setup.py', 'install'], name='Install'),
            pony.TestCommand([self.context.python, 'tests/run.py'], name='Run tests', run_cwd=None),
            ]

if __name__ == '__main__':
    build = PonyBuild()
    sys.exit(build.execute(sys.argv))
