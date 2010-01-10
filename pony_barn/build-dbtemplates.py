import sys
from base_django import DjangoHgBuild
from pony_barn import client as pony

class PonyBuild(DjangoHgBuild):

    def __init__(self):
        super(PonyBuild, self).__init__()
        self.repo_url = "http://bitbucket.org/jezdez/django-dbtemplates"
        self.name = "django-dbtemplates"
        self.package_name = 'dbtemplates'
        self.installed_apps = ['dbtemplates']

if __name__ == '__main__':
    build = PonyBuild()
    sys.exit(build.execute(sys.argv))