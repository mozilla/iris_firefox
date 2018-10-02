# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
from packaging.version import Version, InvalidVersion

logger = logging.getLogger(__name__)

version_key = 'versions'
operator_key = 'operator'


def find_str(s, char):
    """Finds a substring in a string.

    :param s: String you are searching in.
    :param char: String you are searching for.
    :return: If the substring is found it returns the index of the first occurrence, otherwise returns -1.
    """
    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index + len(char)] == char:
                    return index

            index += 1

    return -1


def parse_versions(input_str):
    """Convert a string into a list of versions.

    :param input_str: Input string. Examples of accepted formats:
    '60', '>60', '<60', '>=60', '<=60', '!=60', '60-63'. A '60' version will automatically be converted into '60.0.0'.
    :return: A dictionary containing a list of versions and the comparison operator. If the input string doesn't
    respect the accepted format it will return None.

    Examples:

    input_string = '60-60.1', output is {'operator': '-', 'versions': [<Version('60')>, <Version('60.1')>]}
    input_string = '>=60', output is {'operator': '>=', 'versions': [<Version('60')>]}
    input_string = '>=<60', output is None.
    """

    result = {}
    valid_operators = ['>', '<', '>=', '<=', '!=']

    if input_str is None or input_str == '':
        return

    if '-' in input_str:
        versions_list = input_str.split('-')
        if len(versions_list) > 2:
            return
        else:
            try:

                v_list = [Version(versions_list[0]), Version(versions_list[1])]
                result[version_key] = v_list
                result[operator_key] = '-'
                return result

            except InvalidVersion:
                return
    try:

        result[version_key] = Version(input_str)
        result[operator_key] = '='
        return result

    except InvalidVersion:
        op_list = []
        for op in valid_operators:
            if find_str(input_str, op) == 0:
                op_list.append(op)

        op = max(op_list)
        try:
            result[version_key] = Version(input_str.replace(op, '', 1))
            result[operator_key] = op

        except InvalidVersion:
            return

    return result


def check_version(version, running_condition):
    """
    :param version: Current firefox version.
    :param running_condition: Input string. Examples of accepted formats:
    '60', '>60', '<60', '>=60', '<=60', '!=60', '60-63'. A '60' version will automatically be converted into '60.0.0'.
    :return: returns True if condition between versions is met, otherwise returns False.
    """

    current_version = Version(version)
    version_dict = parse_versions(running_condition)

    if version_dict is not None:
        if version_dict[operator_key] == '>':
            return current_version > version_dict[version_key]
        if version_dict[operator_key] == '<':
            return current_version < version_dict[version_key]
        if version_dict[operator_key] == '>=':
            return current_version >= version_dict[version_key]
        if version_dict[operator_key] == '<=':
            return current_version <= version_dict[version_key]
        if version_dict[operator_key] == '!=':
            return current_version != version_dict[version_key]
        if version_dict[operator_key] == '-':
            return version_dict[version_key][0] <= current_version <= version_dict[version_key][1]

    return False


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
            return 'daily', {'branch': 'mozilla-central', 'destination': destination, 'locale': locale}
        else:
            return 'candidate', {'version': version, 'destination': destination, 'locale': locale}
    else:
        if not has_letters(version) or any(x in version for x in ('b', 'esr')):
            return 'candidate', {'version': version, 'destination': destination, 'locale': locale}
        else:
            logger.warning('Version not recognized. Getting latest nightly build ...')
            return 'daily', {'branch': 'mozilla-central', 'destination': destination, 'locale': locale}


def get_latest_scraper_details(channel):
    """Generate scraper details for the latest available Firefox version based on the channel provided as input."""
    channel = map_latest_release_options(channel)
    if channel == 'nightly':
        return 'daily', {'branch': 'mozilla-central'}
    else:
        return 'candidate', {'version': channel}


def get_version_from_path(path):
    """Extracts a Firefox version from a path.

    Example:
    for input: '/Users/username/workspace/iris/firefox-62.0.3-build1.en-US.mac.dmg' output is '62.0.3'
    """
    new_str = path[path.find('-') + 1: len(path)]
    return new_str[0:new_str.find('-')]
