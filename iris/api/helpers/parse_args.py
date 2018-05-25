# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import argparse
import logging
import os

import iris.firefox.downloader as fd

logger = logging.getLogger(__name__)


def parse_args():
    home = os.path.expanduser('~')
    release_choice, _, test_default = fd.FirefoxDownloader.list()
    release_choice.append('local')

    log_level_strings = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']

    def log_level_string_to_int(log_level_string):
        if log_level_string not in log_level_strings:
            logger.error('Invalid choice: %s (choose from %s)', log_level_string, log_level_strings)
            exit(1)

        log_level_int = getattr(logging, log_level_string, logging.INFO)
        assert isinstance(log_level_int, int)
        return log_level_int

    parser = argparse.ArgumentParser(description='Run Iris testsuite', prog='iris')
    parser.add_argument('-d', '--directory',
                        help='Directory where tests are located',
                        type=str, metavar='test_directory',
                        default=os.path.join('tests'))
    parser.add_argument('-t', '--test',
                        help='Test name, directory or path to a file containing a custom list of tests',
                        type=str, metavar='test_name.py')
    parser.add_argument('-i', '--level',
                        help='Set the logging output level',
                        type=log_level_string_to_int,
                        dest='level',
                        default='INFO')
    parser.add_argument('-w', '--workdir',
                        help='Path to working directory',
                        type=os.path.abspath,
                        action='store',
                        default='%s/.iris' % home)
    parser.add_argument('-f', '--firefox',
                        help=('Firefox version to test. It can be one of {%s}, a package file, '
                              'or a build directory (default: "%s")') % (','.join(release_choice), test_default),
                        action='store',
                        default=test_default)
    parser.add_argument('-l', '--locale',
                        help='Locale to use for Firefox',
                        type=str,
                        action='store',
                        default='en-US')
    parser.add_argument('-m', '--mouse',
                        help='Change mouse speed',
                        type=float,
                        action='store',
                        default=0.5)
    parser.add_argument('-o', '--override',
                        help='Override disabled tests',
                        action='store_true')
    return parser.parse_args()
