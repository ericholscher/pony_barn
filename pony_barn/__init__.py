import os
import glob

from django.conf import settings
from django.utils import importlib

# Built-in reg

class BaseReg(object):

    DEFAULT = {}
    CLASS_NAME = None
    AUTO_IMPORT = None
    _reg = {}

    def __init__(self):
        self._myreg = self._reg[self.name] = {}

    def register(self, format, module, reg=None):
        """"Register a new router.

        ``module`` should be the fully qualified module name
        for the router.

        If ``reg`` is provided, the registration will be added
        to the provided dictionary.

        If ``reg`` is not provided, the registration will be made
        directly into the global register of reg. Adding reg
        directly is not a thread-safe operation.
        """
        module = importlib.import_module(module)
        if reg is None:
            self._myreg[format] = module
        else:
            reg[format] = module

    def unregister(self, format):
        "Unregister a given router. This is not a thread-safe operation."
        del _reg[format]

    def get(self, format):
        if not self._myreg:
            self._load()
        if self.CLASS_NAME:
            return getattr(self._myreg[format], self.CLASS_NAME)
        else:
            return self._myreg[format]


    def get_formats(self):
        if not self._myreg:
            self._load()
        return self._myreg.keys()

    def _load(self):
        """
        Register built-in and settings-defined reg. This is done lazily so
        that user code has a chance to (e.g.) set up custom settings without
        needing to be careful of import order.
        """
        self._myreg
        reg = {}
        for format in self.DEFAULT:
            self.register(format, self.DEFAULT[format], reg)
        if hasattr(settings, "%s_MODULES" % self.name):
            for format in getattr(settings, '%s_MODULES' % self.name):
                dic = getattr(settings, '%s_MODULES' % self.name)
                register(format, dic[format], reg)
        self._myreg = reg
        self.autodiscover()

    def autodiscover(self):
        if self.AUTO_IMPORT:
            from django.db.models.loading import get_apps, get_models
            path = importlib.import_module(self.AUTO_IMPORT).__path__[0]
            for app in glob.glob(os.path.join(path, '*.py')):
                try:
                    app = app.split('.py')[0]
                    app = app.split('/')[-1]
                    if '_' not in app:
                        mod = '%s.%s' % (self.AUTO_IMPORT, app)
                        self.register(app, mod)
                except ImportError, e:
                    print e


class PonyReg(BaseReg):
    name = "pony"
    CLASS_NAME = 'PonyBuild'
    AUTO_IMPORT = "pony_barn"

loading = PonyReg()