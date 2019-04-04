# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
import os

from src.core.util.arg_parser import get_core_args
from src.core.util.path_manager import PathManager

logger = logging.getLogger(__name__)
core_args = get_core_args()


def load_app(app: str = None):
    if app is None:
        logger.warning('No application provided. Launching Firefox application by default')
        app = core_args.application

    app_dir = os.path.join(PathManager.get_module_dir(), 'targets', app)
    if os.path.exists(app_dir):
        logger.debug('%s application module found!' % app)
        return True

    logger.critical('Iris doesn\'t contain %s application module' % app)
    return False


def str_to_test_path_list(app: str, test_path_arg: str):
    test_path_list = []
    test_list = test_path_arg.split(',')
    for test in test_list:
        test_path_list.append(os.path.join(PathManager.get_tests_dir(), app, test))
    return test_path_list


def get_app_test_directory():
    app = core_args.application
    if load_app(app):
        include = core_args.test
        exclude = core_args.exclude

        test_list = []

        tests_directory = os.path.join(PathManager.get_tests_dir(), app)
        logger.debug('Path %s found. Checking content ...', tests_directory)
        for dir_path, sub_dirs, all_files in PathManager.sorted_walk(tests_directory):
            for current_file in all_files:
                current_full_path = os.path.join(dir_path, current_file)
                if current_file.endswith('.py') and not current_file.startswith(
                        '__') and include in current_full_path:
                    if exclude == '' or exclude not in current_full_path:
                        test_list.append(current_full_path)

        if len(test_list) == 0:
            logger.error('Directory %s does not contain test files. Exiting program ...' % tests_directory)
            exit(1)
        else:
            logger.info('List of all tests found: [%s]' % ', '.join(map(str, test_list)))

        return test_list
