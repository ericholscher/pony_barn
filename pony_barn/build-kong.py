import sys
from base_django import DjangoGitBuild
from pony_barn import client as pony

class PonyBuild(DjangoGitBuild):

    def __init__(self):
        super(PonyBuild, self).__init__()
        self.repo_url = "git://github.com/ericholscher/django-kong"
        self.name = "django-kong"
        self.package_name = 'kong'
        self.required = ['django', 'twill', 'mimeparse']
        self.installed_apps = ['kong']

if __name__ == '__main__':
    build = PonyBuild()
    sys.exit(build.execute(sys.argv))
