# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
import os
import shutil
import subprocess
from distutils import dir_util
from distutils.spawn import find_executable
from enum import Enum

import mozversion
from mozdownload import FactoryScraper, errors
from mozinstall import install, get_binary
from mozrunner import FirefoxRunner, errors as run_errors
from mozprofile import Profile as MozProfile

from src.core.api.mouse import mouse
from src.core.api.mouse.mouse import mouse_reset
from src.core.api.os_helpers import OSHelper
from src.core.util.path_manager import PathManager
from targets.firefox.firefox_ui.helpers.general import confirm_firefox_launch
from targets.firefox.firefox_ui.helpers.keyboard_shortcuts import maximize_window
from src.core.util.arg_parser import get_core_args

from src.core.api.errors import APIHelperError

logger = logging.getLogger(__name__)
CHANNELS = ('beta', 'release', 'nightly', 'esr', 'dev')
DEFAULT_FIREFOX_TIMEOUT = 10

default_preferences = {  # Don't automatically update the application
        'app.update.disabledForTesting': True,
        # Don't restore the last open set of tabs if the browser has crashed
        'browser.sessionstore.resume_from_crash': False,
        # Don't check for the default web browser during startup
        'browser.shell.checkDefaultBrowser': False,
        # Don't warn on exit when multiple tabs are open
        'browser.tabs.warnOnClose': False,
        # Don't warn when exiting the browser
        'browser.warnOnQuit': False,
        # Don't send Firefox health reports to the production server
        'datareporting.healthreport.documentServerURI': 'http://%(server)s/healthreport/',
        # Skip data reporting policy notifications
        'datareporting.policy.dataSubmissionPolicyBypassNotification': False,
        # Only install add-ons from the profile and the application scope
        # Also ensure that those are not getting disabled.
        # see: https://developer.mozilla.org/en/Installing_extensions
        'extensions.enabledScopes': 5,
        'extensions.autoDisableScopes': 10,
        # Don't send the list of installed addons to AMO
        'extensions.getAddons.cache.enabled': False,
        # Don't install distribution add-ons from the app folder
        'extensions.installDistroAddons': False,
        # Don't automatically update add-ons
        'extensions.update.enabled': False,
        # Don't open a dialog to show available add-on updates
        'extensions.update.notifyUser': False,
        # Enable test mode to run multiple tests in parallel
        'focusmanager.testmode': True,
        # Enable test mode to not raise an OS level dialog for location sharing
        'geo.provider.testing': True,
        # Suppress delay for main action in popup notifications
        'security.notification_enable_delay': 0,
        # Suppress automatic safe mode after crashes
        'toolkit.startup.max_resumed_crashes': -1,
        # Don't send Telemetry reports to the production server. This is
        # needed as Telemetry sends pings also if FHR upload is enabled.
        'toolkit.telemetry.server': 'http://%(server)s/telemetry-dummy/',
    }


class Profiles(str, Enum):
    """Profile types.

    BRAND_NEW       -   A completely new profile from scratch.
    LIKE_NEW        -   Profile that has had minimal configuration, but would be set up to avoid things like the default
                        browser dialog (browser.shell.checkDefaultBrowser;false); dealing with different warnings
                        (browser.tabs.warnOnClose;false), (browser.tabs.warnOnCloseOtherTabs;false),
                        (browser.warnOnQuit;false) and possibly first-run tour items.
    TEN_BOOKMARKS   -   Identical to LIKE_NEW but has had the activity of bookmarking ten sites.
    DEFAULT         -   We will make LIKE_NEW the default profile.
    """
    BRAND_NEW = 'brand_new'
    LIKE_NEW = 'like_new'
    TEN_BOOKMARKS = 'ten_bookmarks'
    DEFAULT = 'like_new'


class FirefoxProfile:
    """Profile options available to tests.

    With the exception of BRAND_NEW, they are pre-configured, zipped profiles that are part of the source tree,
    unzipped and uniquely created for each test. Profiles are saved to the current run directory, and each is named
    after the test it was created for.
    """

    _profiles = []

    @staticmethod
    def _get_staged_profile(profile_name, path):
        """
        Internal-only method used to extract a given profile.
        :param profile_name:
        :param path:
        :return:
        """
        staged_profiles = os.path.join(PathManager.get_module_dir(), 'targets', 'firefox', 'firefox_app', 'profiles')

        sz_bin = find_executable('7z')
        logger.debug('Using 7zip executable at "%s"' % sz_bin)

        zipped_profile = os.path.join(staged_profiles, '%s.zip' % profile_name.value)

        cmd = [sz_bin, 'x', '-y', '-bd', '-o%s' % staged_profiles, zipped_profile]
        logger.debug('Unzipping profile with command "%s"' % ' '.join(cmd))
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            logger.error('7zip failed: %s' % repr(e.output))
            raise Exception('Unable to unzip profile.')
        logger.debug('7zip succeeded: %s' % repr(output))

        from_directory = os.path.join(staged_profiles, profile_name.value)
        to_directory = path
        logger.debug('Creating new profile: %s' % to_directory)

        dir_util.copy_tree(from_directory, to_directory)

        try:
            shutil.rmtree(from_directory)
        except WindowsError:
            logger.debug('Error, can\'t remove orphaned directory, leaving in place.')

        resource_fork_folder = os.path.join(staged_profiles, '__MACOSX')
        if os.path.exists(resource_fork_folder):
            try:
                shutil.rmtree(resource_fork_folder)
            except WindowsError:
                logger.debug('Error, can\'t remove orphaned directory, leaving in place.')

        return to_directory

    @staticmethod
    def make_profile(profile_type: Profiles = None, preferences: dict = None):
        """Internal-only method used to create profiles on disk.

        :param profile_type: Profile Type (Profiles.BRAND_NEW, Profiles.LIKE_NEW, Profiles.TEN_BOOKMARKS, Profiles.DEFAULT)
        :param preferences: A dictionary containing profile preferences
        """
        if profile_type is None:
            profile_type = Profiles.DEFAULT

        if preferences is None:
            if profile_type is Profiles.BRAND_NEW:
                preferences = default_preferences
            else:
                preferences = {}

        test_root = PathManager.get_current_tests_directory()
        current_test = os.environ.get('CURRENT_TEST')
        test_path = current_test.split(test_root)[1].split('.py')[0][1:]
        profile_path = os.path.join(PathManager.get_current_run_dir(), test_path, 'profile')

        if not os.path.exists(profile_path):
            os.makedirs(profile_path)

        if profile_type is Profiles.BRAND_NEW:
            logger.debug('Creating brand new profile: %s' % profile_path)
        elif profile_type in (Profiles.LIKE_NEW, Profiles.TEN_BOOKMARKS):
            logger.debug('Creating new profile from %s staged profile.' % profile_type.value.upper())
            profile_path = FirefoxProfile._get_staged_profile(profile_type, profile_path)
        else:
            raise ValueError('No profile found: %s' % profile_type.value)

        return MozProfile(profile=profile_path, preferences=preferences)

    @staticmethod
    def _manage_profile_cache(path: str):
        """
        Internal-only method used to delete old profiles that are not in use.
        :param path:
        :return:
        """
        FirefoxProfile._profiles.append(path)
        if len(FirefoxProfile._profiles) > 1:
            shutil.rmtree(FirefoxProfile._profiles.pop(0), ignore_errors=True)


class FirefoxApp:
    def __init__(self, version: str, locale: str):
        path = get_test_candidate(version, locale)
        if path is None:
            raise ValueError

        self.path = path
        self.channel = get_firefox_channel(path)
        self.version = get_firefox_version(path)
        self.latest_version = get_firefox_latest_version(path)
        self.build_id = get_firefox_build_id(path)
        self.locale = locale

    def __str__(self):
        return '(path: {}, channel: {}, version: {}, build: {}, locale: {})'.format(self.path,
                                                                                    self.channel,
                                                                                    self.version,
                                                                                    self.build_id,
                                                                                    self.locale)


class FXRunner:
    def __init__(self, app: FirefoxApp, profile: FirefoxProfile = None):

        if profile is None:
            profile = FirefoxProfile.make_profile()

        self.application = app
        self.profile = profile
        self.runner = self._launch()

    def __str__(self):
        return '(profile: {}, runner: {})'.format(self.profile, self.runner)

    def _launch(self, url: str=None, args=None):
        """Launch the app with optional args for profile, windows, URI, etc.

        :param url: URL to be loaded.
        :param args: Optional list of arguments.
        :return: List of Firefox flags.
        """
        if args is None:
            args = []

        args.append('-foreground')
        args.append('-no-remote')

        if url is None:
            url = 'http://127.0.0.1:{}'.format(get_core_args().port)

        args.append('-new-tab')
        args.append(url)

        process_args = {'stream': None}
        logger.debug('Creating Firefox runner ...')
        try:
            runner = FirefoxRunner(binary=self.application.path, profile=self.profile,
                                   cmdargs=args, process_args=process_args)
            logger.debug('Firefox runner successfully created.')
            logger.debug('Running Firefox with command: "%s"' %
                         ','.join(runner.command))
            return runner
        except run_errors.RunnerNotStartedError:
            raise APIHelperError('Error creating Firefox runner.')

    def start(self, image=None, maximize=True):

        self.runner.start()
        if OSHelper.is_mac():
            mouse_reset()
        confirm_firefox_launch(image)
        if maximize:
            maximize_window()

    def stop(self):
        if self.runner and self.runner.process_handler:
            from targets.firefox.firefox_ui.helpers.keyboard_shortcuts import quit_firefox
            quit_firefox()
            status = self.runner.process_handler.wait(DEFAULT_FIREFOX_TIMEOUT)
            if status is None:
                self.runner.stop()

    def restart(self, image=None):
        self.stop()
        self.start(image, False)


def get_test_candidate(version: str, locale: str) -> str or None:
    """Download and extract a build candidate.

    Build may either refer to a Firefox release identifier, package, or build directory.
    :param: build: str with firefox build
    :return: Installation path for the Firefox App
    """

    if version == 'local':
        candidate = PathManager.get_local_firefox_path()
        if candidate is None:
            logger.critical('Firefox not found. Please download if from https://www.mozilla.org/en-US/firefox/new/')
    else:
        try:
            s_t, s_d = get_scraper_details(version, CHANNELS,
                                           os.path.join(PathManager.get_working_dir(), 'cache'), locale)

            scraper = FactoryScraper(s_t, **s_d)
            firefox_dmg = scraper.download()

            install_dir = install(src=firefox_dmg,
                                  dest=os.path.join(PathManager.get_current_run_dir(),
                                                    'firefox{}{}'.format(normalize_str(version),
                                                                         normalize_str(locale))))

            return get_binary(install_dir, 'Firefox')
        except errors.NotFoundError:
            logger.critical('Specified build {} has not been found. Closing Iris ...'.format(version))
    return None


def normalize_str(main_string: str) -> str:
    """Replace a string with a list of substrings."""
    for elem in ['.', '-']:
        if elem in main_string:
            main_string = main_string.replace(elem, '_')

    return main_string


def has_letters(string: str) -> bool:
    """Check that a string contains letters.

    :param string: String value.
    :return: Returns True if string contains letters, otherwise returns False.
    """
    return any(c.isalpha() for c in string)


def map_latest_release_options(release_option: str) -> str:
    """Overwrite Iris release options to be compatible with mozdownload."""
    if release_option == 'beta':
        return 'latest-beta'
    elif release_option == 'release':
        return 'latest'
    elif release_option == 'esr':
        return 'latest-esr'
    else:
        return 'nightly'


def map_version_to_release_option(version: str) -> str:
    """Returns a release option based on a version provided as input."""
    if not has_letters(version):
        return 'latest'
    elif 'b' in version:
        return 'latest-beta'
    elif 'esr' in version:
        return 'latest-esr'
    else:
        return 'nightly'


def get_latest_scraper_details(channel: str) -> tuple:
    """Generate scraper details for the latest available Firefox version based on the channel provided as input."""
    channel = map_latest_release_options(channel)
    if channel == 'nightly':
        return 'daily', {'branch': 'mozilla-central'}
    else:
        return 'candidate', {'version': channel}


def get_scraper_details(version: str, channels: tuple, destination: str, locale: str) -> tuple:
    """Generate scraper details from version.

    :param version: Can be a Firefox version (ex: 55.0, 55.0b3, etc.) or one of the following options:
                    beta, release, esr, local
    :param channels: A list of channels supported by Iris
    :param destination: Destination path where the Firefox installer will be saved
    :param locale: Firefox locale used
    :return: Scraper type followed by a dictionary that contains the version, destination and locale
    """
    if version in channels:
        version = map_latest_release_options(version)

        if version == 'nightly':
            return 'daily', {'branch': 'mozilla-central',
                             'destination': destination,
                             'locale': locale}
        else:
            return 'candidate', {'version': version,
                                 'destination': destination,
                                 'locale': locale}
    else:
        if '-dev' in version:
            return 'candidate', {'application': 'devedition',
                                 'version': version.replace('-dev', ''),
                                 'destination': destination,
                                 'locale': locale}

        elif not has_letters(version) or any(x in version for x in ('b', 'esr')):
            return 'candidate', {'version': version,
                                 'destination': destination,
                                 'locale': locale}
        else:
            logger.warning('Version not recognized. Getting latest nightly build ...')
            return 'daily', {'branch': 'mozilla-central',
                             'destination': destination,
                             'locale': locale}


def get_version_from_path(path: str) -> str:
    """Extracts a Firefox version from a path.

    Example:
    for input: '/Users/username/workspace/iris/firefox-62.0.3-build1.en-US.mac.dmg' output is '62.0.3'
    """
    new_str = path[path.find('-') + 1: len(path)]
    return new_str[0:new_str.find('-')]


def get_firefox_latest_version(binary: str) -> str or None:
    """Returns Firefox latest available version."""
    if binary is None:
        return None

    channel = get_firefox_channel(binary)
    latest_type, latest_scraper_details = get_latest_scraper_details(channel)
    latest_path = FactoryScraper(latest_type, **latest_scraper_details).filename

    latest_version = get_version_from_path(latest_path)
    logger.info('Latest available version for {} channel is: {}'.format(channel, latest_version))
    return latest_version


def get_firefox_channel(build_path: str) -> str or None:
    """Returns Firefox channel from application repository.

    :param build_path: Path to the binary for the application or Android APK
    file.
    """
    if build_path is None:
        return None

    fx_channel = get_firefox_info(build_path)['application_repository']
    if 'beta' in fx_channel:
        return 'beta'
    elif 'release' in fx_channel:
        return 'release'
    elif 'esr' in fx_channel:
        return 'esr'
    else:
        return 'nightly'


def get_firefox_info(build_path: str) -> str or None:
    """Returns the application version information as a dict with the help of mozversion library.

    :param build_path: Path to the binary for the application or Android APK
    file.
    """
    if build_path is None:
        return None

    # import mozlog
    # mozlog.commandline.setup_logging('mozversion', None, {})
    return mozversion.get_version(binary=build_path)


def get_firefox_version(build_path: str) -> str or None:
    """Returns application version string from the dictionary generated by mozversion library.

    :param build_path: Path to the binary for the application or Android APK
    file.
    """
    if build_path is None:
        return None
    return get_firefox_info(build_path)['application_version']


def get_firefox_build_id(build_path: str) -> str or None:
    """Returns build id string from the dictionary generated by mozversion library.

    :param build_path: Path to the binary for the application or Android APK
    file.
    """
    if build_path is None:
        return None

    return get_firefox_info(build_path)['platform_buildid']


def set_update_channel_pref(path, channel_name):
    base_path = os.path.dirname(path)
    if OSHelper.is_mac():
        base_path = os.path.normpath(os.path.join(base_path, '../Resources/'))
    pref_file = os.path.join(base_path, 'defaults', 'pref', 'channel-prefs.js')
    file_data = 'pref("app.update.channel", "%s");' % channel_name
    if os.path.exists(pref_file):
        logger.debug('Updating Firefox channel-prefs.js file for channel: %s' % channel_name)
        with open(pref_file, 'w') as f:
            f.write(file_data)
            f.close()
    else:
        logger.error('Can\'t find Firefox channel-prefs.js file')
