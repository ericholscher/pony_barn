import sys
from base_django import DjangoBuild
from pony_barn import client as pony

class PonyBuild(DjangoBuild):

    def __init__(self):
        super(PonyBuild, self).__init__()
        self.repo_url = "http://bitbucket.org/jezdez/django-dbtemplates"
        self.name = "django-dbtemplates"
        self.package_name = 'dbtemplates'
        self.installed_apps = ['dbtemplates']

    def define_commands(self):

        self.commands = [ pony.HgClone(self.repo_url, egg=self.package_name),
                     pony.BuildCommand([self.context.python, 'setup.py', 'install'], name='Install'),
                     pony.BuildCommand([self.context.djangoadmin, 'syncdb', '--noinput', '--settings', self.settings_path], name='Syncdb'),
                     pony.TestCommand([self.context.djangoadmin, 'test', self.package_name, '--settings', self.settings_path], name='run tests')
                     ]

if __name__ == '__main__':
    build = PonyBuild()
    sys.exit(build.execute(sys.argv))