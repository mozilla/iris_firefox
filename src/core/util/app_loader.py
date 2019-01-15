# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
import os

from src.core.api.arg_parser import parse_args
from src.core.util.path_manager import PathManager

logger = logging.getLogger(__name__)
args = parse_args()


def load_app(app: str = None):
    if app is None:
        logger.warning('No application provided. Launching Firefox application by default')
        app = args.application

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


def get_app_test_directory(app: str = None):
    tests_to_execute = {'running': [], 'excluded': []}
    if app is None:
        app = args.application
    if load_app(app):
        if args.exclude:
            tests_to_execute['excluded'] = str_to_test_path_list(app, args.exclude)
        if args.test_path:
            tests_to_execute['running'] = str_to_test_path_list(app, args.test_path)
        else:
            tests_to_execute['running'] = [os.path.join(PathManager.get_tests_dir(), app)]

        return tests_to_execute

    tests_to_execute['running'] = [os.path.join(PathManager.get_tests_dir(), app)]
    return tests_to_execute
