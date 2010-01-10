import sys
from base_django import DjangoHgBuild
from pony_barn import client as pony

class PonyBuild(DjangoHgBuild):

    def __init__(self):
        super(PonyBuild, self).__init__()
        self.repo_url = "http://bitbucket.org/andrewgodwin/south"
        self.name = "south"
        self.installed_apps = ['south']
        self.default_db = 'postgres'

if __name__ == '__main__':
    build = PonyBuild()
    sys.exit(build.execute(sys.argv))