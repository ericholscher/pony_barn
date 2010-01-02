import os
import sys
from base_django import DjangoBuild
from pony_build import client as pony

class PonyBuild(DjangoBuild):

    def __init__(self):
        super(PonyBuild, self).__init__()
        self.settings_file = os.path.join(self.directory, 'settings', 'django_settings.py')
        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.repo_url = 'git://github.com/django/django.git'
        self.name = "django"
        self.required = []

    def define_commands(self):
            self.commands = [
                pony.GitClone(self.repo_url),
                pony.TestCommand([self.context.python, 'tests/runtests.py', '--settings', 'django_pony_test_settings'], name='run tests')
             ]

    def get_tags(self):
        # Figure out the python version and tags
        py_version = ".".join(str(p) for p in sys.version_info[:2])
        self.py_name = 'python%s' % py_version

        ret, out, err = pony._run_command(['svn', 'info', 'http://code.djangoproject.com/svn/django/trunk'])
        info = dict(l.split(': ', 1) for l in out.strip().split('\n'))
        revno = info['Last Changed Rev']
        self.tags = [self.py_name, 'svn%s' % revno, 'trunk']

if __name__ == '__main__':
    build = PonyBuild()
    sys.exit(build.execute(sys.argv))
