"""
nose_artifacts.plugin
~~~~~~~~~~~~~~~~

:copyright: 2014 Cumulus Networks, Inc
"""

import os
from nose.plugins import Plugin

class ArtifactsPlugin(Plugin):
    encoding = 'UTF-8'

    def options(self, parser, env):
        Plugin.options(self, parser, env)
        parser.add_option(
            '--artifact-dir', action='store',
            dest='artifact_dir', metavar="DIR",
            help=("Root artifact directory for testrun. [No Default]"))

    def configure(self, options, config):
        Plugin.configure(self, options, config)
        self.config = config
        if not self.enabled:
            return

        root_artifact_dir = options.artifact_dir

        if not root_artifact_dir:
            self.artifact_dir = tempfile.mkdtemp('.artifacts', 'nose.')
        else:
            path = os.path.realpath(os.path.dirname(root_artifact_dir))
            if not os.path.exists(path):
                os.makedirs(path)
            self.artifact_dir = path

    def startTest(self, test):
        # TODO XXX TODO
        # Make a subdirectory from artifact dir with name + timestamp
        # Save this to metadata.curr_artifact_dir
        # If already metadata.curr_artifact_dir, set that to
        # metadata.prev_artifact_dir before setting curr_artifact_dir
        pass
