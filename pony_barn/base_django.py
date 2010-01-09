import os
import sys
from base import BaseBuild
from django.template import Template, Context

class DjangoBuild(BaseBuild):

    def __init__(self):
        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.settings_file = os.path.join(self.directory, 'settings', 'base_settings.py')
        self.required = ['django']
        self.installed_apps = []

    def add_options(self):
        super(DjangoBuild, self).add_options()

        self.cmdline.add_option('-d', '--db',
                           choices=['sqlite', 'postgres', 'mysql'], default='sqlite',
                           help='Which database backend to use.')
        self.cmdline.add_option('--name', default='pony_build_test',
                           help='Database name to use')

    def setup(self):
        #Setup Database
        db = self.options.db
        name = self.options.name
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
        rendered = Template(settings_template).render(context)
        open(settings_dest, 'w').write(rendered)
        open(init_dest, 'w').write('#OMG')
        sys.path.insert(0, dest_dir)
