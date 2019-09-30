# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from moziris.base.testcase import *
from targets.firefox.test_dependencies import *
import inspect
import os

logger = logging.getLogger(__name__)


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
        """Setup method for each test instance."""
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

    @staticmethod
    def get_asset_path(asset_file):
        """Returns a fully-resolved local file path to the test asset."""
        test_path = inspect.stack()[1][1]
        module_path = os.path.split(test_path)[0]
        module_name = os.path.split(test_path)[1].split('.py')[0]
        return os.path.join(module_path, 'assets', module_name, asset_file)
