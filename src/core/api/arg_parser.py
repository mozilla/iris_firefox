# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import argparse
import logging
import os

logger = logging.getLogger(__name__)
iris_args = None


def parse_args():
    global iris_args
    home = os.path.expanduser('~')

    log_level_strings = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']

    def log_level_string_to_int(log_level_string):
        if log_level_string not in log_level_strings:
            logger.error('Invalid choice: %s (choose from %s)', log_level_string, log_level_strings)
            exit(1)

        log_level_int = getattr(logging, log_level_string, logging.INFO)
        assert isinstance(log_level_int, int)
        return log_level_int

    parser = argparse.ArgumentParser(description='Run Iris testsuite', prog='iris')
    app_dir = os.path.join(os.path.realpath(os.path.split(__file__)[0] + '/../..'), 'targets')
    app_list = [f.path for f in os.scandir(app_dir) if f.is_dir()]
    for idx, app in enumerate(app_list):
        app_list[idx] = os.path.basename(os.path.normpath(app))

    parser.add_argument('application', action='store', type=str, help='Application name', choices=app_list)
    parser.add_argument('test_path', action='store', type=str, help='Path to tests module or directory', nargs='?')

    parser.add_argument('-a', '--rerun',
                        help='Rerun last failed tests',
                        action='store_true')
    parser.add_argument('-b', '--highlight',
                        help='Highlight patterns and click actions',
                        action='store_true')
    parser.add_argument('-c', '--clear',
                        help='Clear run data',
                        default=False,
                        action='store_true')
    parser.add_argument('-e', '--email',
                        help='Submit email report',
                        action='store_true')
    parser.add_argument('-g', '--image_debug',
                        help='Temporary flag to hunt down misplaced pattern images.',
                        action='store_true')
    parser.add_argument('-i', '--level',
                        help='Set the logging output level',
                        type=log_level_string_to_int,
                        dest='level',
                        default='INFO')
    parser.add_argument('-k', '--control',
                        help='Display control center',
                        action='store_true')
    parser.add_argument('-m', '--mouse',
                        help='Change mouse speed',
                        type=float,
                        action='store',
                        default=0.5)
    parser.add_argument('-o', '--override',
                        help='Override disabled tests',
                        action='store_true')
    parser.add_argument('-p', '--port',
                        help='Port to use for local web server',
                        type=int,
                        action='store',
                        default=2000)
    parser.add_argument('-r', '--report',
                        help='Report tests to TestRail',
                        action='store_true')
    parser.add_argument('-w', '--workdir',
                        help='Path to working directory',
                        type=os.path.abspath,
                        action='store',
                        default='%s/.iris2' % home)
    parser.add_argument('-x', '--exclude',
                        help='List of test names or directories to exclude',
                        metavar='empty')
    parser.add_argument('-z', '--resize',
                        help='Convert hi-res images to normal',
                        action='store_true')
    if iris_args is None:
        iris_args = parser.parse_args()

    return iris_args
