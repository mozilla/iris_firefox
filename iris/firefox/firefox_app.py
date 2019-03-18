# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os

import logging
from mozdownload import FactoryScraper, errors
from mozinstall import install, get_binary

from iris.api.core.settings import Settings
from iris.api.core.util.core_helper import IrisCore
from iris.api.core.util.parse_args import parse_args
from iris.api.helpers.general import get_firefox_channel, get_firefox_version, get_firefox_build_id

logger = logging.getLogger(__name__)


class FirefoxApp(object):
    def __init__(self):
        path = get_test_candidate()
        if path is None:
            raise ValueError

        self.path = path
        self.channel = get_firefox_channel(path)
        self.version = get_firefox_version(path)
        self.build_id = get_firefox_build_id(path)
        self.locale = parse_args().locale
        self.latest_version = get_firefox_latest_version(path)
        if parse_args().update_channel:
            self.update_channel = parse_args().update_channel
            set_update_channel_pref(self.path, self.update_channel)


def get_local_firefox_path():
    """Checks if Firefox is installed on your machine."""
    paths = {
        'osx': ['/Applications/Firefox.app/Contents/MacOS/firefox',
                '/Applications/Firefox Developer Edition.app/Contents/MacOS/firefox',
                '/Applications/Firefox Nightly.app/Contents/MacOS/firefox'],
        'win': ['C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe',
                'C:\\Program Files (x86)\\Firefox Developer Edition\\firefox.exe',
                'C:\\Program Files (x86)\\Nightly\\firefox.exe',
                'C:\\Program Files\\Mozilla Firefox\\firefox.exe',
                'C:\\Program Files\\Firefox Developer Edition\\firefox.exe',
                'C:\\Program Files\\Nightly\\firefox.exe'],
        'linux': ['/usr/bin/firefox',
                  '/usr/lib/firefox/firefox']
    }
    for path in paths[Settings.get_os()]:
        if os.path.exists(path):
            return path
    return None


def get_test_candidate():
    """Download and extract a build candidate.

    Build may either refer to a Firefox release identifier, package, or build directory.
    :param: build: str with firefox build
    :return: Installation path for the Firefox App
    """

    if parse_args().firefox == 'local':
        candidate = get_local_firefox_path()
        if candidate is None:
            logger.critical('Firefox not found. Please download if from https://www.mozilla.org/en-US/firefox/new/')
    else:
        try:
            locale = 'ja-JP-mac' if parse_args().locale == 'ja' and Settings.is_mac() else parse_args().locale
            type, scraper_details = get_scraper_details(parse_args().firefox, Settings.CHANNELS,
                                                        os.path.join(IrisCore.get_working_dir(), 'cache'),
                                                        locale)
            scraper = FactoryScraper(type, **scraper_details)

            firefox_dmg = scraper.download()
            install_folder = install(src=firefox_dmg,
                                     dest=IrisCore.get_current_run_dir())

            return get_binary(install_folder, 'Firefox')
        except errors.NotFoundError:
            logger.critical('Specified build (%s) has not been found. Closing Iris ...' % parse_args().firefox)
    return None


def has_letters(string):
    """Check that a string contains letters.

    :param string: String value.
    :return: Returns True if string contains letters, otherwise returns False.
    """
    return any(c.isalpha() for c in string)


def map_latest_release_options(release_option):
    """Overwrite Iris release options to be compatible with mozdownload."""
    if release_option == 'beta':
        return 'latest-beta'
    elif release_option == 'release':
        return 'latest'
    elif release_option == 'esr':
        return 'latest-esr'
    else:
        return 'nightly'


def map_version_to_release_option(version):
    """Returns a release option based on a version provided as input."""
    if not has_letters(version):
        return 'latest'
    elif 'b' in version:
        return 'latest-beta'
    elif 'esr' in version:
        return 'latest-esr'
    else:
        return 'nightly'


def get_latest_scraper_details(channel):
    """Generate scraper details for the latest available Firefox version based on the channel provided as input."""
    channel = map_latest_release_options(channel)
    if channel == 'nightly':
        return 'daily', {'branch': 'mozilla-central'}
    else:
        return 'candidate', {'version': channel}


def get_scraper_details(version, channels, destination, locale):
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


def get_version_from_path(path):
    """Extracts a Firefox version from a path.

    Example:
    for input: '/Users/username/workspace/iris/firefox-62.0.3-build1.en-US.mac.dmg' output is '62.0.3'
    """
    new_str = path[path.find('-') + 1: len(path)]
    return new_str[0:new_str.find('-')]


def get_firefox_latest_version(binary):
    """Returns Firefox latest available version."""

    if binary is None:
        return None

    channel = get_firefox_channel(binary)
    latest_type, latest_scraper_details = get_latest_scraper_details(channel)
    latest_path = FactoryScraper(latest_type, **latest_scraper_details).filename

    latest_version = get_version_from_path(latest_path)
    logger.info('Latest available version for %s channel is: %s' % (channel, latest_version))
    return latest_version


def set_update_channel_pref(path, channel_name):
    base_path = os.path.dirname(path)
    if Settings.is_mac():
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
