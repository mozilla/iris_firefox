# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.errors import FindError, APIHelperError
from iris.api.core.mouse import click
from iris.api.core.region import logger, wait


class Step(object):

    def __init__(self, resolution, message):
        self.resolution = resolution
        self.message = message

    def get_resolution(self):
        return self.resolution

    def get_message(self):
        return self.message


def access_and_check_pattern(access_pattern, msg, check_pattern=None, access_type=None):
    """Access and check(if it exists) the patterns received.

    :param access_pattern: pattern to find and access if access_type is not None.
    :param msg: Message to display on test result
    :param check_pattern: pattern to assert after accessing 'find_pattern'.
    :param access_type: action to be performed on the access_pattern image. TODO Add more actions when needed
    :return: None.
    """

    try:
        exists = wait(access_pattern, 10)
        logger.debug('%s pattern is displayed properly.' % access_pattern)
        if access_type and access_type == 'click':
            click(access_pattern)
    except FindError:
        raise APIHelperError(
            'Can\'t find the %s pattern, aborting.' % access_pattern.get_filename())

    if check_pattern:
        try:
            exists = wait(check_pattern, 15)
            logger.debug('%s pattern has been found.' % check_pattern.get_filename())
        except FindError:
            raise APIHelperError('Can\'t find the %s option, aborting.' % check_pattern.get_filename())

    return Step(exists, '%s was accessed and displayed properly.' % msg)
