import sys
import os
import tempfile
import shutil

import pony_barn.client as pony

class BaseBuild(object):
    def __init__(self):
        self.required = []

    def setup(self):
        pass

    def get_tags(self):
        # Figure out the python version and tags
        py_version = ".".join(str(p) for p in sys.version_info[:2])
        self.py_name = 'python%s' % py_version
        self.tags = [self.py_name, 'base_builder']

    def execute(self, argv):
        self.options, self.args = pony.parse_cmdline(argv)

        self.get_tags()
        ###
        self.server_url = 'http://devmason.com/pony_server/xmlrpc'
        if not self.options.force_build:
            if not pony.check(self.name, self.server_url, tags=self.tags):
                print 'check build says no need to build; bye'
                sys.exit(0)

        self.context = pony.VirtualenvContext(self.options.cleanup_temp, self.required)
        self.setup()
        self.define_commands()
        results = pony.do(self.name, self.commands, context=self.context)
        client_info, reslist = results


        if self.options.report:
            print 'Result: %s; sending' % (client_info['success'],)
            pony.send(self.server_url, results, tags=self.tags)
        else:
            print
            print "-"*60
            print 'Build results:'
            print '(not sending build results to server)'
            print
            print "Client info:"
            for (k, v) in client_info.items():
                print "  %s: %s" % (k, v)
            print
            print "Build details:"
            for i, step in enumerate(reslist):
                print "  Step %s: %s" % (i, step['name'])
                for k, v in step.items():
                    print "    %s: %s" % (k, v)

        if not client_info['success']:
            return -1
        return 0
