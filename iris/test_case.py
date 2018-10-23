# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from api.core.local_web import LocalWeb
from api.core.profile import *
from api.helpers.general import *
from asserts import *
from configuration.config_parser import *
from iris.api.core.util.update_rules import *
from iris.test_rail.test_case_results import TestRailTests

logger = logging.getLogger(__name__)


class BaseTest(object):

    def __init__(self, app):
        """Resets test case properties.

        :param app: Instance of the FirefoxApp class.
        """
        self._app = app

        """Test case description."""
        self._meta = ''

        """Firefox version."""
        self._fx_version = ''

        """List of platforms object. E.g: Platform.LINUX, Platform.ALL."""
        self._exclude = []

        """Test case title from test rail."""
        self._test_title = ''

        """List of test results."""
        self._results = []

        """Test case's start time."""
        self._start_time = 0

        """Test case's end time."""
        self._end_time = 0

        """Test case's outcome."""
        self._outcome = 'PASSED'

        """List of test case prefs."""
        self._prefs = {}

        """Path to the Firefox profile."""
        self._profile_path = None

        """Browser channel."""
        self._channel = Settings.CHANNELS

        """Firefox locales. E.g: en-US, zh-CN, es-ES, de, fr, ru, ar, ko, pt-PT, vi, pl, tr, ro, ja."""
        self._locale = Settings.LOCALES

        """Supported platforms. E.g: LINUX, MAC, WINDOWS."""
        self._platform = Platform.ALL

        """Test case tags."""
        self._tags = ''

        """Test case id."""
        self._test_case_id = ''

        """Test case suite id."""
        self._test_suite_id = ''

        """Blocker for current test case."""
        self._blocked_by = ''

        """Firefox runner for current test case"""
        self._firefox_runner = None

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, value):
        self._app = value

    @property
    def meta(self):
        return self._meta

    @meta.setter
    def meta(self, value):
        self._meta = value

    @property
    def fx_version(self):
        return self._fx_version

    @fx_version.setter
    def fx_version(self, value):
        self._fx_version = value

    @property
    def exclude(self):
        return self._exclude

    @exclude.setter
    def exclude(self, value):
        self._exclude = value

    @property
    def test_title(self):
        return self._test_title

    @test_title.setter
    def test_title(self, value):
        self._test_title = value

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, value):
        self._results = value

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, value):
        self._end_time = value

    @property
    def outcome(self):
        return self._outcome

    @outcome.setter
    def outcome(self, value):
        self._outcome = value

    @property
    def prefs(self):
        return self._prefs

    @prefs.setter
    def prefs(self, value):
        self._prefs = value

    @property
    def profile_path(self):
        return self._profile_path

    @profile_path.setter
    def profile_path(self, value):
        self._profile_path = value

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        self._channel = value

    @property
    def locale(self):
        return self._locale

    @locale.setter
    def locale(self, value):
        self._locale = value

    @property
    def platform(self):
        return self._platform

    @platform.setter
    def platform(self, value):
        self._platform = value

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = value

    @property
    def test_case_id(self):
        return self._test_case_id

    @test_case_id.setter
    def test_case_id(self, value):
        self._test_case_id = value

    @property
    def test_suite_id(self):
        return self._test_suite_id

    @test_suite_id.setter
    def test_suite_id(self, value):
        self._test_suite_id = value

    @property
    def blocked_by(self):
        return self._blocked_by

    @blocked_by.setter
    def blocked_by(self, value):
        self._blocked_by = value

    @property
    def firefox_runner(self):
        return self._firefox_runner

    @firefox_runner.setter
    def firefox_runner(self, value):
        self._firefox_runner = value

    def add_result(self, result):
        """Setter for the test results property."""
        self.results.append(result)
        self.get_results()

    def get_results(self):
        """Setter for the test outcome property."""
        for result in self.results:
            self.outcome = result.outcome

    def create_collection_test_rail_result(self):
        """Returns the test rail object."""
        test_rail_object = TestRailTests(self.meta, self.test_suite_id, self.blocked_by, self.test_case_id,
                                         self.results)
        return test_rail_object

    def get_test_duration(self):
        """Returns the test duration with 2 decimals precision."""
        return round(self.end_time - self.start_time, 2)

    def add_results(self, outcome, message, actual, expected, error):
        res = Result(outcome, message, actual, expected, error)
        self.add_result(res)

    @staticmethod
    def get_asset_path(asset_file_name):
        """Returns a fully-resolved local file path to the test asset."""
        test_path = inspect.stack()[1][1]
        module_path = os.path.split(test_path)[0]
        module_name = os.path.split(test_path)[1].split('.py')[0]
        return os.path.join(module_path, 'assets', module_name, asset_file_name)

    def get_web_asset_path(self, asset_file_name):
        """Returns a fully-resolved URL to the test asset."""
        test_path = inspect.stack()[1][1]
        test_directory = os.path.split(test_path)[0].split('tests')[1]
        module_name = os.path.split(test_path)[1].split('.py')[0]
        resource = '/tests%s/%s/%s' % (test_directory, module_name, asset_file_name)
        return self.app.base_local_web_url + resource

    @staticmethod
    def get_blank_page_url():
        """Returns a fully-resolved URL to a blank web page."""
        return LocalWeb.BLANK_PAGE

    def set_profile_pref(self, pref):
        """Setter for the prefs property."""
        self._prefs.update(pref)

    def setup(self):
        """ Test case setup
        This might be a good place to declare variables or initialize Fx state.
        Also, by default, a new Firefox instance is created, with a new profile and
        blank URL. If you wish to change this, override this method in your test case.
        If you do override this method in your test case, you *must* call
        BaseTest.setup(self) as the first line in your setup method.
        """

        """Launch with devtools opened by default."""
        self.devtools = False

        """Launch with bookmark import dialog open by default."""
        self.import_wizard = False

        """Launch with JS debugger open by default."""
        self.js_debugger = False

        """Launch with JS console open by default."""
        self.js_console = False

        """Use window controls to force maximum window size."""
        self.maximize_window = True

        """Launch with preference panel open by default."""
        self.preferences = False

        """Launch in permanent private browser mode by default."""
        self.private_browsing = False

        """Launch default window in private browsing mode."""
        self.private_window = False

        """Use default profile template specified by Iris."""
        self.profile = Profile.DEFAULT

        """Launch with Profile Manager open by default."""
        self.profile_manager = False

        """Launch with Firefox safe mode by default."""
        self.safe_mode = False

        """Launch with the results of a provided search term using default search engine."""
        self.search = None

        """Set Firefox as the default browser on the system."""
        self.set_default_browser = False

        """Launch default window with the URL specified.
        Currently this is used by Iris, so it should not be overridden.
        """
        test_name = os.path.splitext(os.path.split(IrisCore.get_current_module())[1])[0]
        parameters = '?current=%s&total=%s&title=%s' % (self.app.current_test, self.app.total_tests, test_name)
        self.url = self.app.base_local_web_url + parameters

        """Launch window with dimensions of width and height, separated by the 
        lowercase letter x.
        e.g. 600x800
        Will automatically set self.maximize_window to False
        """
        self.window_size = None

        """Temporary code used to write a pref file, not used otherwise."""
        self.set_profile_pref({'iris.enabled': True})

        return

    def run(self):
        """This will be overwritten with your test logic."""
        return

    def teardown(self):
        """This might be a good place to clean up what was done."""
        return
