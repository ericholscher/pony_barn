import sys
from pony_barn import client as pony
from base import GitBuild

class PonyBuild(GitBuild):

    def __init__(self):
        super(PonyBuild, self).__init__()
        self.name = "surlex"
        self.repo_url = 'git://github.com/codysoyland/surlex.git'

if __name__ == '__main__':
    build = PonyBuild()
    sys.exit(build.execute(sys.argv))