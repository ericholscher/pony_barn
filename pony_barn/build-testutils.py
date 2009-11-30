import sys
from base_django import DjangoBuild
from pony_build import client as pony

class TestUtilsBuild(DjangoBuild):

    def __init__(self):
        super(TestUtilsBuild, self).__init__()
        self.repo_url = "git://github.com/ericholscher/django-test-utils"
        self.name = "django-test-utils"
        self.package_name = 'test_app'
        self.required = ['django']
        self.installed_apps = ['test_utils', 'test_project.polls', 'test_project.test_app']

    def define_commands(self):

        self.commands = [ pony.GitClone(self.repo_url),
                     pony.BuildCommand([self.context.python, 'setup.py', 'install'], name='Install'),
                     pony.BuildCommand([self.context.djangoadmin, 'syncdb', '--noinput', '--settings', 'django_pony_test_settings'], name='Install'),
                     pony.TestCommand([self.context.djangoadmin, 'test', self.package_name, '--settings', 'django_pony_test_settings'], name='run tests')
                     ]

if __name__ == '__main__':
    build = TestUtilsBuild()
    sys.exit(build.execute(sys.argv))