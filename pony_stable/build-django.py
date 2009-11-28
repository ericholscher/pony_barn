import os
import sys
from base import BaseBuild
from pony_build import client as pony

class DjangoBuild(BaseBuild):

    def __init__(self):
        super(DjangoBuild, self).__init__()
        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.repo_url = 'git://github.com/django/django.git'
        self.name = "django"

    def define_commands(self):
            self.commands = [
                pony.GitClone(self.repo_url),
                pony.TestCommand([self.context.python, '../tests/runtests.py', '--settings', 'django_pony_test_settings'], name='run tests', run_cwd='django')
             ]

    def setup(self):
        # Create the settings file
        dest_dir = os.path.join(self.context.tempdir, 'lib', self.py_name, 'site-packages')
        settings_dest = os.path.join(dest_dir, 'django_pony_test_settings.py')
        init_dest = os.path.join(dest_dir, '__init__.py')
        open(settings_dest, 'w').write("DATABASE_ENGINE='sqlite3'")
        open(init_dest, 'w').write('#OMG')
        sys.path.insert(0, dest_dir)

if __name__ == '__main__':
    build = DjangoBuild()
    sys.exit(build.execute(sys.argv))
