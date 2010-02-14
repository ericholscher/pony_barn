import sys
from base_django import DjangoGitBuild
from pony_barn import client as pony

class PonyBuild(DjangoGitBuild):
    def __init__(self):
        super(PonyBuild, self).__init__()
        self.repo_url = "git://github.com/ericholscher/django_inspect"
        self.name = "django_inspect"
        self.package_name = 'django_inspect'
        self.installed_apps = ['django_inspect']

if __name__ == '__main__':
    build = PonyBuild()
    sys.exit(build.execute(sys.argv))
