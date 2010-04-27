"""
Client library for pony-build.

See http://github.com/ericholscher/pony_barn/.
"""

import datetime
import sys
import subprocess
import xmlrpclib
import tempfile
import shutil
import os, os.path
import time
import traceback
from optparse import OptionParser

import pip

DEFAULT_CACHE_DIR='~/.pony-build'

def guess_cache_dir(dirname):
    parent = os.environ.get('PONY_BUILD_CACHE', DEFAULT_CACHE_DIR)
    parent = os.path.expanduser(parent)
    result = os.path.join(parent, dirname)
    return result

def _run_command(command_list, cwd=None, variables=None):
    print command_list
    environment = os.environ.copy()
    environment['PIP_DOWNLOAD_CACHE'] = '/tmp/pip/download'
    environment['PYTHONPATH'] = "%s:%s" % (os.getcwd(), environment['PYTHONPATH'])
    if variables:
        x = []
        for cmd in command_list:
            x.append(cmd)
        command_list = x

    try:
        p = subprocess.Popen(command_list, shell=False, cwd=cwd,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             env=environment)

        out, err = p.communicate()
        ret = p.returncode
    except:
        out = ''
        err = traceback.format_exc()
        ret = -1

    return (ret, out, err)

class Context(object):
    def __init__(self):
        self.history = []
        self.start_time = self.end_time = None
        self.build_dir = None

    def initialize(self):
        self.start_time = time.time()

    def finish(self):
        self.end_time = time.time()

    def start_command(self, command):
        if self.build_dir:
            os.chdir(self.build_dir)

    def end_command(self, command):
        self.history.append(command)

    def update_client_info(self, info):
        info['duration'] = self.end_time - self.start_time

class CurrentDirectoryContext(Context):
    def __init__(self, cleanup=True):
        Context.__init__(self)
        self.cleanup = cleanup

    def initialize(self):
        Context.initialize(self)
        print "Using the current directory (%s) as my working dir" % os.getcwd()

class TempDirectoryContext(Context):
    def __init__(self, cleanup=True):
        Context.__init__(self)
        self.cleanup = cleanup

    def initialize(self):
        Context.initialize(self)
        self.tempdir = tempfile.mkdtemp()
        self.cwd = os.getcwd()

        print 'changing to temp directory:', self.tempdir
        os.chdir(self.tempdir)

class VirtualenvContext(Context):
    def __init__(self, always_cleanup=True, use_site_packages=False, dependencies=[], **kwargs):
        Context.__init__(self)
        self.cleanup = always_cleanup
        self.dependencies = dependencies
        base_build = kwargs['base_build']

        # Create the virtualenv. Have to do this here so that commands can use
        # VirtualenvContext.python (etc) to get at the right python.
        import virtualenv

        self.tempdir = tempfile.mkdtemp()

        print 'creating virtualenv'
        if use_site_packages:
            _run_command([base_build.py_name, '-m', 'virtualenv', self.tempdir])
        else:
            _run_command([base_build.py_name, '-m', 'virtualenv', '--no-site-packages', self.tempdir])

        # calculate where a few things live so we can easily shell out to 'em
        self.python = os.path.join(self.tempdir, 'bin', 'python')
        self.djangoadmin = os.path.join(self.tempdir, 'bin', 'django-admin.py')
        self.easy_install = os.path.join(self.tempdir, 'bin', 'easy_install')
        self.pip = os.path.join(self.tempdir, 'bin', 'pip')

    def initialize(self):
        self.start_time = datetime.datetime.now()
        print 'changing to temp directory:', self.tempdir
        self.cwd = os.getcwd()
        os.chdir(self.tempdir)

        # install pip, then use it to install any packages desired
        print 'installing pip'
        _run_command([self.easy_install, '-U', 'pip==dev'])
        for dep in self.dependencies:
            print "installing", dep
            _run_command([self.pip, 'install', '-U', '-I'] + dep.split())

    def finish(self):
        os.chdir(self.cwd)
        try:
            self.end_time = datetime.datetime.now()
        finally:
            if self.cleanup:
                print 'removing', self.tempdir
                shutil.rmtree(self.tempdir, ignore_errors=True)

    def update_client_info(self, info):
        #Context.update_client_info(self, info)
        info['start_time'] = str(self.start_time)
        info['end_time'] = str(self.end_time)
        info['tempdir'] = self.tempdir
        info['virtualenv'] = True

class BaseCommand(object):
    def __init__(self, command_list, name='', run_cwd=None):
        self.command_list = command_list
        if name:
            self.command_name = name
        self.run_cwd = run_cwd

        self.status = None
        self.output = None
        self.errout = None
        self.duration = None

        self.variables = None

    def set_variables(self, v):
        self.variables = dict(v)

    def run(self, context):
        start = time.time()

        (ret, out, err) = _run_command(self.command_list, cwd=self.run_cwd,
                                       variables=self.variables)

        self.status = ret
        self.output = out
        self.errout = err
        end = time.time()

        self.duration = end - start

    def success(self):
        return self.status == 0

    def get_results(self):
        results = dict(status=self.status,
                       output=self.output,
                       errout=self.errout,
                       command=str(self.command_list),
                       type=self.command_type,
                       name=self.command_name,
                       duration=self.duration)
        return results

class SetupCommand(BaseCommand):
    command_type = 'setup'
    command_name = 'setup'

class BuildCommand(BaseCommand):
    command_type = 'build'
    command_name = 'build'

class TestCommand(BaseCommand):
    command_type = 'test'
    command_name = 'test'


class VCSClone(SetupCommand):
    command_name = 'checkout'

    def __init__(self, repository, branch='master', cache_dir=None,
                 use_cache=True, egg=None, **kwargs):
        SetupCommand.__init__(self, [], **kwargs)
        self.repository = repository
        self.branch = branch
        self.egg = egg

        self.use_cache = use_cache
        self.cache_dir = cache_dir

        self.duration = -1
        self.version_info = ''

        self.results_dict = {}

    def run(self, context):
        if self.use_cache:
            cache_dir = self.cache_dir
            if not cache_dir:
                cache_dir = guess_cache_dir(self.egg)
        vcs = pip.vcs.get_backend(self.vcs)
        vcs_repo = vcs("%s+%s#egg=%s" % (self.vcs, self.repository, self.egg))
        try:
            if os.path.exists(cache_dir):
                try:
                    if vcs.name is 'git':
                        _run_command(['git', 'clean', '-f', self.cache_dir])
                        vcs_repo.update(cache_dir, ['origin/master'])
                    else:
                        #pip doesn't use the second arg.
                        vcs_repo.update(cache_dir, [])
                except Exception, e:
                    #If an update failed, still run.
                    #This allows for running tests offline
                    print "Updating Repo Failed: %s" % e
            else:
                vcs_repo.obtain(cache_dir)
            self.status = 0
        except Exception, e:
            print "Exception on checkout: %s" % e
            self.status = 1

        context.build_dir = cache_dir

    def get_results(self):
        self.results_dict['out'] = self.results_dict['errout'] = ''
        self.results_dict['command'] = 'Clone(%s, %s)' % (self.repository,
                                                             self.branch)
        self.results_dict['status'] = self.status
        self.results_dict['type'] = self.command_type
        self.results_dict['name'] = self.command_name

        self.results_dict['version_type'] = self.vcs
        if self.version_info:
            self.results_dict['version_info'] = self.version_info

        return self.results_dict

class GitClone(VCSClone):
    vcs = "git"

class HgClone(VCSClone):
    vcs = "hg"

class SvnUpdate(VCSClone):
    vcs = "svn"


def get_hostname():
    import socket
    return socket.gethostname()

def get_arch():
    import distutils.util
    return distutils.util.get_platform()

###

def _send(server, info, results):
    print 'connecting to', server
    s = xmlrpclib.ServerProxy(server, allow_none=True)
    s.add_results(info, results)

def do(name, commands, context=None, arch=None, stop_if_failure=True):
    reslist = []

    if context:
        context.initialize()

    for c in commands:
        print 'running: %s (%s)' % (c.command_name, c.command_type)
        if context:
            context.start_command(c)
        c.run(context)
        if context:
            context.end_command(c)

        reslist.append(c.get_results())

        if stop_if_failure and not c.success():
            break

    if context:
        context.finish()

    if arch is None:
        arch = get_arch()

    success = all([ c.success() for c in commands ])

    client_info = dict(package=name, arch=arch, success=success)
    if context:
        context.update_client_info(client_info)

    return (client_info, reslist)

def send(server_url, x, hostname=None, tags=()):
    client_info, reslist = x
    if hostname is None:
        import socket
        hostname = socket.gethostname()

    client_info['host'] = hostname
    client_info['tags'] = tags

    print 'using server URL:', server_url
    _send(server_url, client_info, reslist)

def check(name, server_url, tags=(), hostname=None, arch=None, reserve_time=0):
    if hostname is None:
        hostname = get_hostname()

    if arch is None:
        arch = get_arch()

    client_info = dict(package=name, host=hostname, arch=arch, tags=tags)
    s = xmlrpclib.ServerProxy(server_url, allow_none=True)
    (flag, reason) = s.check_should_build(client_info, True, reserve_time)
    return flag
