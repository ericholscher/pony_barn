import os
import sys
from base import BaseBuild
from pony_build import client as pony

SETTINGS = """
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    },
    'other': {
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST_NAME': 'other_db'
    }
}
"""


class DjangoBuild(BaseBuild):

    def __init__(self):
        super(DjangoBuild, self).__init__()
        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.repo_url = 'git://github.com/django/django.git'
        self.name = "django"

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

    def setup(self):
        # Create the settings file
        dest_dir = os.path.join(self.context.tempdir, 'lib', self.py_name, 'site-packages')
        settings_dest = os.path.join(dest_dir, 'django_pony_test_settings.py')
        init_dest = os.path.join(dest_dir, '__init__.py')
        open(settings_dest, 'w').write(SETTINGS)
        open(init_dest, 'w').write('#OMG')
        sys.path.insert(0, dest_dir)

if __name__ == '__main__':
    build = DjangoBuild()
    sys.exit(build.execute(sys.argv))
