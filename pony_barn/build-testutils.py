import sys
from base import BaseBuild
from pony_barn import client as pony

class PonyBuild(BaseBuild):

    def __init__(self):
        super(PonyBuild, self).__init__()
        self.repo_url = "git://github.com/ericholscher/django-test-utils"
        self.name = "django-test-utils"
        self.package_name = "test_utils"
        self.required = ['django', 'twill', 'BeautifulSoup']

    def define_commands(self):

        self.commands = [ pony.GitClone(self.repo_url, egg=self.package_name),
                        pony.TestCommand([self.context.python, 'test_project/runtests.py', '--settings', 'test_project.settings'], name='run tests')
                     ]

if __name__ == '__main__':
    build = PonyBuild()
    sys.exit(build.execute(sys.argv))
