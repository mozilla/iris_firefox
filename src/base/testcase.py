# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
import unittest

mylogger = logging.getLogger(__name__)


class BaseTest():

    def setup(self):
        "setup method for each test instance"
        return

    @classmethod
    def setup_class(cls):
        return

    @classmethod
    def teardown_class(cls):
        return

    def setup_method(self, method):
        return


    def teardown_method(self, method):
        return
