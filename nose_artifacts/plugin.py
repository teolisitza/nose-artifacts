"""
nose_artifacts.plugin
~~~~~~~~~~~~~~~~

:copyright: 2014 Cumulus Networks, Inc
"""

# Use testconfig plugin <--> test communication
import testconfig

# Plugin base class
from nose.plugins import Plugin

# Make simple wrappers with `partial` method
import functools

# Standard imports
import os
import tempfile
import atexit

import logging
log = logging.getLogger('nose_artifacts.plugin')

def remove_if_empty(arg, dirname, fnames):
    if not fnames:
        os.removedirs(dirname)

def prune_empty_dirs(dirname):
    if os.path.exists(dirname):
        log.info('Cleaning up empty artifact dirs under %s' % dirname)
    else:
        # artifact dir does not exist
        # probably already cleaned up
        return

    os.path.walk(dirname, remove_if_empty, None)
    if not os.path.exists(dirname):
        log.info('%s was removed because all sub-directories were empty.' \
                 '' % dirname)

class ArtifactsPlugin(Plugin):
    name = "artifacts"
    encoding = 'UTF-8'

    def options(self, parser, env):
        Plugin.options(self, parser, env)
        parser.add_option(
            '--artifact-dir', action='store',
            dest='artifact_dir', metavar="DIR",
            help=("Root artifact directory for testrun. [Default " \
                  "is new sub-dir under /tmp]"))

    def configure(self, options, config):
        Plugin.configure(self, options, config)
        self.config = config

        if not self.enabled:
            return

        root_artifact_dir = options.artifact_dir

        # Make a temp directory if one is not provided
        if not root_artifact_dir:
            self.artifact_dir = tempfile.mkdtemp('.artifacts', 'nose.')
        else:
            # If provided, make the path if it does not exist
            path = os.path.realpath(root_artifact_dir)
            if not os.path.exists(path):
                os.makedirs(path)
            self.artifact_dir = path

        # Even if we get ^C bombed, still clean this directory
        # upon interpreter exit.
        atexit.register(prune_empty_dirs, self.artifact_dir)

    def startTest(self, test):
        """ Create directory for upcoming test and update current
            and previous pointers to artifact directories.

        Directory will be named <ROOT_ARTIFACT_DIR>/<TEST_ID>,
        but if that already exists, then we'll try
        <ROOT_ARTIFACT_DIR>/<TEST_ID>.1, just like log files. """

        path = orig_path = os.path.join(self.artifact_dir, test.id())
        if os.path.exists(path):
            test_id = 1
            path += '%s.%d' % (orig_path, test_id)
            while os.path.exists(path):
                test_id += 1
                path += '%s.%d' % (orig_path, test_id)
        os.makedirs(path)

        cfg = testconfig.config
        metadata = cfg.get('metadata')
        if not metadata:
            metadata = cfg['metadata'] = {}
        else:
            if 'curr_artifact_dir' in metadata:
                log.debug('Setting previous artifact directory: ' \
                          '%s' % metadata['curr_artifact_dir'])
                metadata['prev_artifact_dir'] = metadata['curr_artifact_dir']

        log.info('Current artifact directory: %s' % path)
        metadata['curr_artifact_dir'] = path

    def finalize(self, result):
        prune_empty_dirs(self.artifact_dir)
