# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.errors import FindError
from iris.api.core.mouse import click
from iris.api.core.region import logger, wait
from iris.asserts import assert_true


def access_and_check_pattern(test_case, access_pattern, msg, check_pattern=None, access_type=None):
    """Access and check(assert) the patterns received.

    :param test_case: test object used to add test step resolution
    :param access_pattern: pattern to find and access if acces_type is not None.
    :param msg: Message to display on test result
    :param check_pattern: pattern to assert after accessing 'find_pattern'.
    :param access_type: action to be performed on the access_pattern image. TODO Add more actions when needed
    :return: None.
    """

    try:
        exists = wait(access_pattern, 10)
        logger.debug('%s pattern was displayed properly.' % access_pattern)
        if access_type is not None and access_type == 'click':
            click(access_pattern)
        assert_true(test_case, exists, '%s was displayed properly.' % msg)
    except FindError:
        raise FindError(
            'Can\'t find the %s pattern, aborting.' % access_pattern.get_filename())

    if check_pattern is not None:
        try:
            wait(check_pattern, 15)
            logger.debug('%s option has been found.' % check_pattern.get_filename())
        except FindError:
            raise FindError('Can\'t find the %s option, aborting.' % check_pattern.get_filename())
