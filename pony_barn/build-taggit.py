import sys
from base_django import DjangoGitBuild
from pony_barn import client as pony

class PonyBuild(DjangoGitBuild):
    def __init__(self):
        super(PonyBuild, self).__init__()
        self.repo_url = "git://github.com/alex/django-taggit.git"
        self.name = "django-taggit"
        self.package_name = 'taggit'
        self.installed_apps = ['taggit', 'taggit.tests']

if __name__ == '__main__':
    build = PonyBuild()
    sys.exit(build.execute(sys.argv))
