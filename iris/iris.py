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
        self.args = parser.parse_args()

        self.module_dir = get_module_dir()
        self.platform = get_platform()
        self.os = get_os()

        test_runner.run(self)


Iris()
