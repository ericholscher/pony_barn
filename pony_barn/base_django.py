import os
import sys
from base import BaseBuild
from django.template import Template, Context

class DjangoBuild(BaseBuild):

    def __init__(self):
        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.settings_file = os.path.join(self.directory, 'settings', 'base_settings.py')
        self.required = ['django']

    def setup(self):
        # Create the settings file
        dest_dir = os.path.join(self.context.tempdir, 'lib', self.py_name, 'site-packages')
        settings_dest = os.path.join(dest_dir, 'django_pony_test_settings.py')
        init_dest = os.path.join(dest_dir, '__init__.py')
        settings_template = open(self.settings_file).read()
        rendered = Template(settings_template).render(Context({'more_installed': self.installed_apps}))
        open(settings_dest, 'w').write(rendered)
        open(init_dest, 'w').write('#OMG')
        sys.path.insert(0, dest_dir)
