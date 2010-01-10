import sys
from base import BaseBuild
from pony_barn import client as pony

class PonyBuild(BaseBuild):

    def __init__(self):
        super(PonyBuild, self).__init__()
        self.repo_url = "git://github.com/mintchaos/django_compressor.git"
        self.name = "django_compressor"
        self.required = ['django']

    def define_commands(self):

        self.commands = [ pony.GitClone(self.repo_url, egg=self.get_name()),
                        pony.TestCommand([self.context.python, 'tests/manage.py', 'test', '--settings', 'tests.settings'], name='run tests')
                     ]

if __name__ == '__main__':
    build = PonyBuild()
    sys.exit(build.execute(sys.argv))
