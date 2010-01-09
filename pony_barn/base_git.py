import sys
from pony_barn import client as pony
from base import BaseBuild

class GitBuild(BaseBuild):

    def define_commands(self):
        self.commands = [
            pony.GitClone(self.repo_url, egg=self.get_name()),
            pony.BuildCommand([self.context.python, 'setup.py', 'install'], name='Install'),
            pony.TestCommand([self.context.python, 'setup.py', 'test'], name='Run tests', run_cwd=None),
            ]
