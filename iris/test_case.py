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
        self.fx_version = ''
        self.exclude = []
        self.test_title = ''
        self.results = []
        self.start_time = 0
        self.end_time = 0
        self.outcome = 'PASSED'

    def get_test_title(self):
        return self.test_title

    def set_test_title(self, test_title):
        self.test_title = test_title

    def add_result(self, result):
        self.results.append(result)
        self.get_results()

    def get_results(self):
        for result in self.results:
            self.outcome = result.outcome

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

    def get_asset_path(self, path):
        return os.path.join(path, 'assets/')

    def setup(self):
        """ Test case setup
        This might be a good place to declare variables or initialize Fx state.
        Also, by default, a new Firefox instance is created, with a blank profile and URL.
        If you wish to change this, override this method in your test case.
        """
        self.profile = Profile.DEFAULT
        launch_firefox(path=self.app.fx_path, profile=self.profile, url='about:blank')
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
        self.reset_variables()
        quit_firefox()
        return
