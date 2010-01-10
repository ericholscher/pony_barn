import sys
from pony_barn import client as pony
from base import BaseBuild

class HgBuild(BaseBuild):
    """
    A build that checks out from a hg repo and runs setup.py test on your repo
    """

    def define_commands(self):
        self.commands = [
            pony.HgClone(self.repo_url, egg=self.get_name()),
            pony.BuildCommand([self.context.python, 'setup.py', 'install'], name='Install'),
            pony.TestCommand([self.context.python, 'setup.py', 'test'], name='Run tests', run_cwd=None),
            ]
