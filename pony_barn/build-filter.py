import sys
from base_django import DjangoGitBuild
from pony_barn import client as pony


class PonyBuild(DjangoGitBuild):

    def __init__(self):
        super(PonyBuild, self).__init__()
        self.repo_url = "git://github.com/alex/django-filter.git"
        self.name = "django-filter"
        self.package_name = 'django_filters'
        self.installed_apps = ['django_filters', 'django_filters.tests']

if __name__ == '__main__':
    build = PonyBuild()
    sys.exit(build.execute(sys.argv))
