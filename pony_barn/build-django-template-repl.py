import sys
from base_django import DjangoGitBuild
from pony_barn import client as pony

class PonyBuild(DjangoGitBuild):
    def __init__(self):
        super(PonyBuild, self).__init__()
        self.repo_url = 'git://github.com/codysoyland/django-template-repl.git'
        self.name = 'django-template-repl'
        self.package_name = 'template_repl'
        self.installed_apps = ['template_repl']

if __name__ == '__main__':
    build = PonyBuild()
    sys.exit(build.execute(sys.argv))
