# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from api.helpers.general import *
from api.helpers.keyboard_shortcuts import *
from asserts import *
from configuration.config_parser import *

logger = logging.getLogger(__name__)


class BaseTest(object):

    def __init__(self, app):
        self.app = app
        self.reset_variables()

    def reset_variables(self):
        self.meta = ''
        self.exclude = []
        self.test_title = ''
        self.results = []
        self.start_time = 0
        self.end_time = 0
        self.is_complete = False
        self.is_passed = True

    def get_test_title(self):
        return self.test_title

    def set_test_title(self, test_title):
        self.test_title = test_title

    def add_result(self, result):
        self.results.append(result)
        self.get_results()

    def get_results(self):
        for result in self.results:
            if 'FAILED' == result.outcome:
                self.is_complete = True
                self.is_passed = False
                return
        self.is_complete = True
        self.is_passed = True

    def print_results(self):
        for result in self.results:
            if 'ERROR' == result.outcome:
                logger.error('Error encountered in test, outcome: >>> ERROR <<< %s' % '\n' + result.error if
                             result.error else '')
            elif 'FAILED' == result.outcome:
                logger.warning('Step: %s, outcome: >>> %s <<< %s' % (
                    result.message, result.outcome, '\n' + result.error if result.error else ''))
            elif 'PASSED' == result.outcome:
                logger.success('Step: %s, outcome: >>> %s <<<' % (result.message, result.outcome))
        logger.info('%s - >>> %s <<< (Finished in %s second(s))\n' % (
            self.meta, format_outcome(self.is_passed), get_duration(self.start_time, self.end_time)))

    def get_start_time(self):
        return self.start_time

    def set_start_time(self, start_time):
        self.start_time = start_time

    def get_end_time(self):
        return self.end_time

    def set_end_time(self, end_time):
        self.end_time = end_time

    def get_test_duration(self):
        return round(self.end_time - self.start_time, 2)

    def add_results(self, outcome, message, actual, expected, error):
        res = Result(outcome, message, actual, expected, error)
        self.add_result(res)

    @staticmethod
    def _create_unique_profile_name():
        ts = int(time.time())
        profile_name = 'profile_%s' % ts
        return profile_name

    def setup(self):
        """ Test case setup
        This might be a good place to declare variables or initialize Fx state.
        Also, by default, a new Firefox instance is created, with a blank profile and URL.
        If you wish to change this, override this method in your test case.
        """
        launch_firefox(path=self.app.fx_path, profile=self._create_unique_profile_name(), url='about:blank')
        return

    @staticmethod
    def resize_window():
        """ Resize Window
        By default, we will maximize the window.
        If this is not desired, override this method in your test case.
        """
        maximize_window()

    def run(self):
        """This is your test logic."""
        return

    def teardown(self):
        """This might be a good place to clean up what was done."""
        self.print_results()
        self.reset_variables()
        quit_firefox()
        return
