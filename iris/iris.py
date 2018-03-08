# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import test_runner
from api.core import *
from logger.iris_logger import *
import argparse

logger = getLogger(__name__)

class Iris(object):

    def __init__(self):

        self.parse_args()
        self.module_dir = get_module_dir()
        self.platform = get_platform()
        self.os = get_os()

        test_runner.run(self)


    def parse_args(self):

        LOG_LEVEL_STRINGS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']

        def log_level_string_to_int(log_level_string):
            if not log_level_string in LOG_LEVEL_STRINGS:
                logger.error('Invalid choice: %s (choose from %s)', log_level_string, LOG_LEVEL_STRINGS)
                exit(1)

            log_level_int = getattr(logging, log_level_string, logging.INFO)
            assert isinstance(log_level_int, int)
            return log_level_int

        parser = argparse.ArgumentParser(description='Run Iris testsuite', prog='iris')
        parser.add_argument('-d', '--directory',
                            help='Directory where tests are located',
                            type=str, metavar='test_directory',
                            default=os.path.join("tests"))
        parser.add_argument('-t', '--test',
                            help='Test name',
                            type=str, metavar='test_name.py')
        parser.add_argument('-l', '--level',
                            help='Set the logging output level',
                            type=log_level_string_to_int,
                            dest='level',
                            default='INFO')
        """
        # These arguments will be added soon, putting them in now to reserve their flags
        parser.add_argument("-debug", "--debug",
                            help="Enable debug",
                            action="store_true")
        parser.add_argument("-w", "--workdir",
                            help="Path to working directory",
                            type=os.path.abspath,
                            action="store",
                            default="%s/.iris" % home)
        parser.add_argument('-f', '--firefox',
                           help=("Firefox version to test. It can be one of {%s}, a package file, "
                                 "or a build directory (default: `%s`)") % (",".join(release_choice), test_default),
                           action='store',
                           default=test_default)
        parser.add_argument("-l", "--locale",
                            help="Locale to use for Firefox",
                            type=str,
                            action="store",
                            default="en-US")
        """
        self.args = parser.parse_args()
        print self.args


Iris()
