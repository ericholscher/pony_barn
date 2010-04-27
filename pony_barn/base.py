import sys
import os
import tempfile
import shutil
import optparse

import pony_barn.client as pony

class BaseBuild(object):

    def __init__(self):
        self.required = []
        self.tags = []
        self.vcs_list = {
        'git': pony.GitClone,
        'hg': pony.HgClone,
        'svn': pony.SvnUpdate,
        }

    def setup(self):
        "This is where subclasses define extra setup."
        pass

    def define_commands(self):
        "This is where subclasses define how they are run."
        pass

    @property
    def vcs_class(self):
        return self.vcs_list[self.vcs]

    def execute(self, argv):
        self.add_options()
        self.options, self.args = self.cmdline.parse_args(argv)

        if not self.options.server_url:
            self.server_url = 'http://devmason.com/pony_server/xmlrpc'
        else:
            self.server_url = self.options.server_url


        if not self.options.local:
            self.context_class = pony.CurrentDirectoryContext
            self.skip_vcs = True
        else:
            self.context_class = pony.VirtualenvContext
            self.skip_vcs = False

        self.get_tags()
        self.check_build()
        self.context = self.context_class(always_cleanup=self.options.cleanup_temp,
                                              use_site_packages=self.options.site_packages,
                                              dependencies=self.required,
                                              base_build=self)
        self.setup()
        self.define_commands()
        results = pony.do(self.name, self.commands, context=self.context)
        return self.report(results)


    def add_options(self):
        self.cmdline = optparse.OptionParser()
        self.cmdline.add_option('-f', '--force-build', dest='force_build',
                           action='store_true', default=False,
                           help="run a build whether or not it's stale")
        self.cmdline.add_option('-r', '--report', dest='report',
                           action='store_true', default=False,
                           help="report build results to server")
        self.cmdline.add_option('-l', '--local', dest='local',
                           action='store_true', default=True,
                           help="Run the tests in your current directory")
        self.cmdline.add_option('-N', '--no-clean-temp', dest='cleanup_temp',
                           action='store_false', default=True,
                           help='do not clean up the temp directory')
        self.cmdline.add_option('-s', '--server-url', dest='server_url',
                           action='store', default='',
                           help='set pony-build server URL for reporting results')
        self.cmdline.add_option('-v', '--verbose', dest='verbose',
                           action='store_true', default=False,
                           help='set verbose reporting')
        self.cmdline.add_option('-P', '--site-packages', dest='site_packages',
                           action='store_true', default=False,
                           help='Use the system site packages')

    def get_tags(self):
        # Figure out the python version and tags
        py_version = ".".join(str(p) for p in sys.version_info[:2])
        self.py_name = 'python%s' % py_version
        self.tags.extend([self.py_name, 'base_builder'])

    def check_build(self):
        try:
            if not self.options.force_build:
                if not pony.check(self.name, self.server_url, tags=self.tags):
                    print 'check build says no need to build; bye'
                    sys.exit(0)
        except Exception, e:
            #Don't fail on network error etc.
            print "Check should build Exception: %s" % e

    def report(self, results):
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


    def get_name(self):
        if hasattr(self, 'package_name'):
            return self.package_name
        else:
            return self.name


class NoseBuild(BaseBuild):
    """
    A build that runs nosetests at the top of the source tree.
    """

    def define_commands(self):
        self.commands = [
            self.vcs_class(self.repo_url, egg=self.get_name()),
            pony.BuildCommand([self.context.python, 'setup.py', 'install'], name='Install from source'),
            pony.TestCommand([os.path.join(self.context.tempdir, 'bin', 'nosetests')], name="Run Nose Tests")
            ]


class VCSBuild(BaseBuild):
    """
    A build that checks out from a git repo and runs setup.py test on your repo
    """

    def define_commands(self):
        self.commands = [
            self.vcs_class(self.repo_url, egg=self.get_name()),
            pony.BuildCommand([self.context.python, 'setup.py', 'install'], name='Install'),
            pony.TestCommand([self.context.python, 'setup.py', 'test'], name='Run tests', run_cwd=None),
            ]


class GitBuild(VCSBuild):
    """
    A build that checks out from a git repo and runs setup.py test on your repo
    """
    vcs = 'git'

class HgBuild(VCSBuild):
    """
    A build that checks out from a hg repo and runs setup.py test on your repo
    """
    vcs = 'hg'

class SvnBuild(VCSBuild):
    """
    A build that checks out from a svn repo and runs setup.py test on your repo
    """
    vcs = 'svn'