# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import sys

import firefox.app as fa
import firefox.downloader as fd
import firefox.extractor as fe

from api.core.profile import *
from api.helpers.general import *
from asserts import *
from configuration.config_parser import *

from firefox.app import FirefoxApp
from iris.test_rail.test_case_results import TestRailTests
logger = logging.getLogger(__name__)


class BaseTest(object):

    def __init__(self, app):
        self.app = app
        self.reset_variables()
        self.args = parse_args()
        self.os = Settings.get_os()
        self.module_dir = get_module_dir()

    def reset_variables(self):
        self.meta = ''
        self.fx_version = ''
        self.exclude = []
        self.test_title = ''
        self.results = []
        self.start_time = 0
        self.end_time = 0
        self.outcome = 'PASSED'
        self.prefs = []
        self.profile_path = None
        self.channel = FirefoxApp.CHANNELS
        self.locale = FirefoxApp.LOCALES
        self.platform = Platform.ALL
        self.test_case_id = ''
        self.test_suite_id = ''
        self.blocked_by = ''

    def get_test_meta(self):
        return self.meta

    def get_test_case_id(self):
        return self.test_case_id

    def get_test_title(self):
        return self.test_title

    def get_test_results(self):
        return self.results

    def add_result(self, result):
        self.results.append(result)
        self.get_results()

    def get_results(self):
        for result in self.results:
            self.outcome = result.outcome

    def create_collection_test_rail_result(self):
        test_rail_object = TestRailTests(self.meta, self.test_suite_id, self.blocked_by, self.test_case_id, self.get_test_results())
        return test_rail_object

    def set_test_title(self, test_title):
        self.test_title = test_title

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

    def get_asset_path(self, asset_file_name):
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

    def set_profile_pref(self, pref):
        self.prefs.append(pref)

    def get_test_candidate(self, build):
        """Download and extract a build candidate.
        Build may either refer to a Firefox release identifier, package, or build directory.
        :param:
            build: str with firefox build
        :return:
            FirefoxApp object for test candidate
        """
        version = '50.0'
        if os.path.isdir(build):
            candidate_app = fa.FirefoxApp(build, Settings.get_os(), False)
            return candidate_app
        else:
            platform = fd.FirefoxDownloader.detect_platform()
            if platform is None:
                logger.error('Unsupported platform: "%s"' % sys.platform)
                sys.exit(5)

            # `build` may refer to a build reference as defined in FirefoxDownloader,
            # a local Firefox package as produced by `mach build`, or a local build tree.
            if build in fd.SpecificFirefoxDownloader.build_urls:
                # Download test candidate by Firefox release ID
                logger.info('Downloading Firefox "%s" build for platform "%s"' % (build, platform))
                fdl = fd.SpecificFirefoxDownloader(self.args.workdir, cache_timeout=1 * 60 * 60)
                build_archive_file = fdl.download(build, self.args.locale, version, platform)
                if build_archive_file is None:
                    self.finish(code=-1)
                # Extract candidate archive
                candidate_app = fe.extract(build_archive_file, Settings.get_os(), self.args.workdir,
                                           cache_timeout=1 * 60 * 60)
                candidate_app.package_origin = fdl.get_download_url(build, self.args.locale, version, platform)
            elif os.path.isfile(build):
                # Extract firefox build from archive
                logger.info('Using file "%s" as Firefox package' % build)
                candidate_app = fe.extract(build, Settings.get_os(), self.args.workdir, cache_timeout=1 * 60 * 60)
                candidate_app.package_origin = build
                logger.debug('Build candidate executable is "%s"' % candidate_app.exe)
            elif os.path.isfile(os.path.join(build, 'mach')):
                logger.info('Using Firefox build tree at `%s`' % build)
                dist_globs = sorted(glob.glob(os.path.join(build, 'obj-*', 'dist')))
                if len(dist_globs) == 0:
                    logger.critical('"%s" looks like a Firefox build directory, but can\'t find a build in it' % build)
                    self.finish(code=5)
                logger.debug('Potential globs for dist directory: %s' % dist_globs)
                dist_dir = dist_globs[-1]
                logger.info('Using "%s" as build distribution directory' % dist_dir)
                if 'apple-darwin' in dist_dir.split('/')[-2]:
                    # There is a special case for OS X dist directories:
                    # FirefoxApp expects OS X .dmg packages to contain the .app folder inside
                    # another directory. However, that directory isn't there in build trees,
                    # thus we need to point to the parent for constructing the app.
                    logger.info('Looks like this is an OS X build tree')
                    candidate_app = fa.FirefoxApp(os.path.abspath(os.path.dirname(dist_dir)), Settings.get_os(), True)
                    candidate_app.package_origin = os.path.abspath(build)
                else:
                    candidate_app = fa.FirefoxApp(os.path.abspath(dist_dir), Settings.get_os(), True)
                    candidate_app.package_origin = os.path.abspath(build)
            else:
                logger.critical('"%s" specifies neither a Firefox release, package file, or build directory' % build)
                logger.critical('Valid Firefox release identifiers are: %s' % ', '.join(fd.FirefoxDownloader.list()[0]))
                self.finish(5)

            logger.debug('Build candidate executable is "%s"' % candidate_app.exe)
            if candidate_app.platform != platform:
                logger.warning('Platform mismatch detected')
                logger.critical('Running a Firefox binary for "%s" on a "%s" platform will probably fail' %
                                (candidate_app.platform, platform))
            return candidate_app

    def finish(self, code=0):
        """
        All exit points of Iris need to call this function in order to exit properly.
        """
        if hasattr(self, 'process_list'):
            logger.debug('There are %s queued process(es) to terminate.' % len(self.process_list))
            for process in self.process_list:
                logger.debug('Terminating process.')
                process.terminate()
                process.join()
        sys.exit(code)

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
        test_name = os.path.splitext(os.path.split(get_current_module())[1])[0]
        parameters = '?current=%s&total=%s&title=%s' % (self.app.current_test, self.app.total_tests, test_name)
        self.url = self.app.base_local_web_url + parameters

        """Launch window with dimensions of width and height, separated by the 
        lowercase letter x.
        e.g. 600x800
        Will automatically set self.maximize_window to False
        """
        self.window_size = None

        """Temporary code used to write a pref file, not used otherwise."""
        self.set_profile_pref('iris.enabled;true')

        return

    def run(self):
        """This is your test logic."""
        return

    def teardown(self):
        """This might be a good place to clean up what was done."""
        self.reset_variables()
        return
