# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import test_runner
from api.core import *
from logger.iris_logger import *
import argparse

class Iris(object):

    def __init__(self):
        logger = getLogger(__name__)

        parser = argparse.ArgumentParser(description='Run Iris testsuit', prog='iris')
        parser.add_argument('-d', '--directory', type=str, metavar='tests_directory', help='Directory where tests are located')
        parser.add_argument('-t', '--test', type=str, metavar='test_name.py', help='Test name')
        args = parser.parse_args()

        tests_list = []
        tests_package = []

        if args.directory:
            tests_directory =  os.path.join(os.path.split(__file__)[0], args.directory.strip())
            if (os.path.isdir(tests_directory)):
                logger.info("Path %s found. Checking content ...", tests_directory)
                for file in os.listdir(tests_directory):
                    if file.endswith(".py") and not file.startswith("__init__"):
                        tests_list.append(os.path.splitext(file)[0])
                if len(tests_list) == 0:
                    logger.error("Directory %s does not contain test files. Exiting program ...", tests_directory)
                    exit(1)
                else:
                    tests_package = tests_directory
                    logger.info("Module for tests: %s", tests_package)
                    logger.info("List of tests to execute: [%s]" % ', '.join(map(str, tests_list)))
            else:
                logger.error("Path: %s does not exist. Exiting program ...", tests_directory)
                exit(1)

        self.module_dir = get_module_dir()
        self.platform = get_platform()
        self.os = get_os()
        self.tests_package = tests_package
        self.tests_list = tests_list

        test_runner.run(self)


Iris()
