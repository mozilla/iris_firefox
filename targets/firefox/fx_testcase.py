# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys

from src.base.testcase import *
from src.configuration.config_parser import logger
from targets.firefox.firefox_ui import *
from targets.firefox.test_assert import *
from targets.firefox.firefox_ui.helpers.keyboard_shortcuts import *
from targets.firefox.firefox_ui.web_links.local_web import LocalWeb
from targets.firefox.firefox_app.fx_browser import Profiles
from src.core.api.settings import _Settings
from targets.firefox.firefox_ui.bookmarks import *



class FirefoxTest(BaseTest):


    outcome = ''
    test_results = []

    @classmethod
    def setup_class(cls):
        return

    @classmethod
    def teardown_class(cls):
        return

    def setup_method(self, method):
      pass

    def setup(self):
        "setup method for each test instance"
        return

    def teardown_method(self, method):
        # self.test_results.clear()
        return

    def add_result(self, result):
        """Setter for the test results property."""
        self.test_results.append(result)

    def add_results(self, result):
        """Create test result object."""
        self.add_result(result)
        if 'ERROR' == result.outcome:
            logger.error('>>> ERROR <<< Error encountered in test %s' % '\n' + result.error if
                         result.error else '')
        elif 'FAILED' == result.outcome:
            logger.warning('>>> FAILED <<< Step %s: %s - [Actual]: %s [Expected]: %s %s'
                           % (len(self.test_results), result.message, result.actual, result.expected,
                              '\n' + result.error if result.error else ''))
        elif 'PASSED' == result.outcome:
            logger.info('>>> PASSED <<< Step %s: %s' % (len(self.test_results), result.message))

        self.outcome = result.outcome
