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
from iris.test_dependencies import *

logger = logging.getLogger(__name__)


class BaseTest(object):

    def __init__(self):
        self.meta = ''
        self.fx_version = ''
        self.enabled = True
        self.test_title = ''
        self.exclude = []
        self.results = []
        self.start_time = 0
        self.end_time = 0
        self.outcome = 'PASSED'
        self.prefs = {}
        self.profile_path = None
        self.channel = Settings.CHANNELS
        self.locale = Settings.LOCALES
        self.platform = Platform.ALL
        self.tags = ''
        self.test_case_id = ''
        self.test_suite_id = ''
        self.blocked_by = {'id': '', 'platform': []}
        self.firefox_runner = None
        self.browser = None
        self.base_local_web_url = ''
        self.index = 1
        self.total_tests = 1

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
        blocked_by = self.blocked_by['id'] if all(k in self.blocked_by for k in ("id", "platform")) else ''
        test_rail_object = TestRailTests(self.meta, self.test_suite_id, blocked_by, self.test_case_id,
                                         self.results)
        return test_rail_object

    def get_test_duration(self):
        """Returns the test duration with 2 decimals precision."""
        return round(self.end_time - self.start_time, 2)

    def add_results(self, result):
        """Create test result object."""
        self.add_result(result)
        if 'ERROR' == result.outcome:
            logger.error('>>> ERROR <<< Error encountered in test %s' % '\n' + result.error if
                         result.error else '')
        elif 'FAILED' == result.outcome:
            logger.warning('>>> FAILED <<< Step %s: %s - [Actual]: %s [Expected]: %s %s'
                           % (len(self.results), result.message, result.actual, result.expected,
                              '\n' + result.error if result.error else ''))
        elif 'PASSED' == result.outcome:
            logger.success('>>> PASSED <<< Step %s: %s' % (len(self.results), result.message))

    @staticmethod
    def get_asset_path(asset_file_name):
        """Returns a fully-resolved local file path to the test asset."""
        test_path = inspect.stack()[1][1]
        module_path = os.path.split(test_path)[0]
        module_name = os.path.split(test_path)[1].split('.py')[0]
        return os.path.join(module_path, 'assets', module_name, asset_file_name)

    @staticmethod
    def get_web_asset_path(asset_file_name):
        """Returns a fully-resolved URL to the test asset."""
        test_path = inspect.stack()[1][1]
        test_directory = os.path.split(test_path)[0].split('tests')[1]
        module_name = os.path.split(test_path)[1].split('.py')[0]
        resource = '/tests%s/%s/%s' % (test_directory, module_name, asset_file_name)
        return 'http://127.0.0.1:%s' % parse_args().port + resource

    @staticmethod
    def get_blank_page_url():
        """Returns a fully-resolved URL to a blank web page."""
        return LocalWeb.BLANK_PAGE

    def set_profile_pref(self, pref):
        """Setter for the prefs property."""
        self.prefs.update(pref)

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
        parameters = '?current=%s&total=%s&title=%s' % (self.index, self.total_tests, test_name)
        self.url = 'http://127.0.0.1:%s' % parse_args().port + parameters

        """Launch window with dimensions of width and height, separated by the 
        lowercase letter x.
        e.g. 600x800
        Will automatically set self.maximize_window to False
        """
        self.window_size = None

        """Temporary code used to write a pref file, not used otherwise."""
        self.set_profile_pref({'iris.enabled': True}),
        self.set_profile_pref({'extensions.privatebrowsing.notification': True}),
        self.set_profile_pref({'browser.contentblocking.introCount': 20})

        return

    def run(self):
        """This will be overwritten with your test logic."""
        return

    def teardown(self):
        """This might be a good place to clean up what was done."""
        return
