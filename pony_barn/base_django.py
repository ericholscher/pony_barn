import os
import sys
from base import BaseBuild
from pony_barn import client as pony
from django.template import Template, Context
from django.conf import settings


class DjangoBuild(BaseBuild):
    """
    A build that sets up a django settings file for you
    """

    def __init__(self):
        super(DjangoBuild, self).__init__()
        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.settings_file = os.path.join(self.directory, 'settings', 'base_settings.py')
        self.required = ['django']
        self.installed_apps = []

    def add_options(self):
        super(DjangoBuild, self).add_options()

        self.cmdline.add_option('-d', '--db',
                           choices=['sqlite', 'postgres', 'mysql'], default=None,
                           help='Which database backend to use.')
        self.cmdline.add_option('--name', default='pony_build_test',
                           help='Database name to use')

    def setup(self):
        #Setup Database
        name = self.options.name

        db = self.options.db
        if db is None:
            if hasattr(self, 'default_db'):
                print "Using Default DB"
                db = self.default_db
            else:
                db = 'sqlite'

        if db == 'sqlite':
            self.db_engine = 'sqlite3'
            self.db_name = name
            self.db_user = ''
            self.db_pass = ''
        elif db == 'postgres':
            self.db_engine = 'postgresql_psycopg2'
            self.db_name = name
            self.db_user = ''
            self.db_pass = ''
        elif db == 'mysql':
            self.db_engine = 'mysql'
            self.db_name = name
            self.db_user = ''
            self.db_pass = ''

        self.tags.append(db)

        # Create the settings file
        self.settings_path = "pony_barn_test_settings"
        dest_dir = os.path.join(self.context.tempdir, 'lib', self.py_name, 'site-packages')
        settings_dest = os.path.join(dest_dir, '%s.py' % self.settings_path)
        init_dest = os.path.join(dest_dir, '__init__.py')
        settings_template = open(self.settings_file).read()
        context = Context({
            'more_installed': self.installed_apps,
            'db_engine': self.db_engine,
            'db_name': self.db_name,
            'db_user': self.db_user,
            'db_pass': self.db_pass,
        })
        #Templates needs settings... :/
        if not settings.configured:
            settings.configure()
        rendered = Template(settings_template).render(context)
        open(settings_dest, 'w').write(rendered)
        open(init_dest, 'w').write('#OMG')
        sys.path.insert(0, dest_dir)


class DjangoVCSBuild(DjangoBuild):
    """
    A build that checkouts out from a repo and then runs manage.py test
    on your application
    """

    def define_commands(self):
        self.commands = [
            self.vcs_class(self.repo_url, egg=self.get_name()),
            pony.BuildCommand([self.context.python, 'setup.py', 'install'], name='Install'),
            pony.BuildCommand([self.context.djangoadmin, 'syncdb', '--noinput', '--settings', self.settings_path], name='Syncdb'),
            pony.TestCommand([self.context.djangoadmin, 'test', self.get_name(), '--settings', self.settings_path], name='run tests')
            ]


class DjangoGitBuild(DjangoVCSBuild):
    """
    A build that checkouts out from a git repo and then runs manage.py test
    on your application
    """
    vcs = 'git'

class DjangoHgBuild(DjangoVCSBuild):
    """
    A build that checkouts out from a hg repo and then runs manage.py test
    on your application
    """
    vcs = 'hg'

class DjangoSvnBuild(DjangoVCSBuild):
    """
    A build that checkouts out from a svn repo and then runs manage.py test
    on your application
    """
    vcs = 'svn'