import os
import sys
from base import BaseBuild
from pony_barn import client as pony


# DRL_FIXME: Fetch/setup a simple Solr for testing?
# DRL_FIXME: Add pysolr dependency.
# DRL_FIXME: Add Whoosh dependency.


class PonyBuild(BaseBuild):
    def __init__(self):
        super(DjangoBuild, self).__init__()
        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.repo_url = 'git://github.com/toastdriven/django-haystack.git'
        self.name = "haystack"
    
    def define_commands(self):
        self.commands = [
            pony.GitClone(self.repo_url),
            pony.TestCommand([self.context.djangoadmin, 'test', 'core', '--settings', 'settings'], name='run core tests'),
            # pony.TestCommand([self.context.python, '../tests/run_all_tests.sh'], name='run tests', run_cwd='haystack')
        ]
    
    # DRL_TODO: Setup Solr (and possibly Whoosh) here.
    # def setup(self):
    #     # Create the settings file
    #     dest_dir = os.path.join(self.context.tempdir, 'lib', self.py_name, 'site-packages')
    #     settings_dest = os.path.join(dest_dir, 'django_pony_test_settings.py')
    #     init_dest = os.path.join(dest_dir, '__init__.py')
    #     open(settings_dest, 'w').write("DATABASE_ENGINE='sqlite3'")
    #     open(init_dest, 'w').write('#OMG')
    #     sys.path.insert(0, dest_dir)


if __name__ == '__main__':
    build = PonyBuild()
    sys.exit(build.execute(sys.argv))
