import sys
from pony_barn import client as pony
from base import HgBuild

class PonyBuild(HgBuild):

    def __init__(self):
        super(PonyBuild, self).__init__()
        self.name = "nose"
        self.repo_url = 'http://bitbucket.org/jpellerin/nose/overview/'
        self.package_name = "nose"

if __name__ == '__main__':
    build = PonyBuild()
    sys.exit(build.execute(sys.argv))
