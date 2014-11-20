"""
nose_artifacts
~~~~~~~~~

:copyright: 2014 Cumulus Networks.
:license: BSD
"""

import testconfig
import functools

def _get_config_metadata_var(name):
    cfg = testconfig.config
    if not cfg:
        return None

    metadata = cfg.get('metadata')
    if not metadata:
        return None

    return metadata.get(name)

get_curr_artifact_dir = functools.partial(_get_config_metadata_var,
                                          name="curr_artifact_dir")
get_prev_artifact_dir = functools.partial(_get_config_metadata_var,
                                          name="prev_artifact_dir")
