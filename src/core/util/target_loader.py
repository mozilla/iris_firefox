# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
import os

from src.core.util.arg_parser import get_core_args
from src.core.util.path_manager import PathManager

logger = logging.getLogger(__name__)
core_args = get_core_args()


def load_target(target: str = None):
    """Checks if provided target exists."""
    if target is None:
        logger.warning('No target provided. Launching Firefox target by default')
        target = core_args.target

    target_dir = os.path.join(PathManager.get_module_dir(), 'targets', target)
    if os.path.exists(target_dir):
        logger.debug('%s target module found!' % target)
        return True

    logger.critical('Iris doesn\'t contain %s target module' % target)
    return False


def get_target_test_directory():
    """Collects tests based on include/exclude criteria and selected target."""
    target = core_args.target
    test_list = []

    if load_target(target):
        include = core_args.test
        exclude = core_args.exclude

        tests_dir = os.path.join(PathManager.get_tests_dir(), target)
        logger.debug('Path %s found. Checking content ...', tests_dir)
        for dir_path, sub_dirs, all_files in PathManager.sorted_walk(tests_dir):
            for current_file in all_files:
                current_full_path = os.path.join(dir_path, current_file)
                if current_file.endswith('.py') and not current_file.startswith('__') and include in current_full_path:
                    if exclude == '' or exclude not in current_full_path:
                        test_list.append(current_full_path)

        if len(test_list) == 0:
            logger.error('\'%s\' does not contain tests based on your search criteria. Exiting program.' % tests_dir)
        else:
            logger.debug('List of all tests found: [%s]' % ', '.join(map(str, test_list)))

    return test_list
