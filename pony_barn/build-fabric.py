import sys
from pony_barn import client as pony
from base_git import GitBuild

class PonyBuild(GitBuild):

    def __init__(self):
        super(PonyBuild, self).__init__()
        self.name = "fabric"
        self.repo_url = 'git://github.com/ericholscher/fabric.git'
        self.package_name = "fabric"

if __name__ == '__main__':
    build = PonyBuild()
    sys.exit(build.execute(sys.argv))
