import os, sys
from pony_barn import client as pony
from base import BaseBuild

class PonyBuild(BaseBuild):

    def __init__(self):
        super(PonyBuild, self).__init__()
        self.name = "jinja2"
        self.required = ['nose']
        self.repo_url = 'http://dev.pocoo.org/hg/jinja2-main'

    def define_commands(self):
        self.commands = [
            pony.HgClone(self.repo_url, egg=self.get_name()),
            pony.BuildCommand([self.context.python, 'setup.py', 'install'], name='Install from source'),
            pony.TestCommand([os.path.join(self.context.tempdir, 'bin', 'nosetests')], name="Run Tests", run_cwd='tests')
            ]

if __name__ == '__main__':
    build = PonyBuild()
    sys.exit(build.execute(sys.argv))
