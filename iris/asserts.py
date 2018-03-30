# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import traceback
from api.helpers.results import *


class Assert(object):

    def __init__(self, outcome, message, actual, expected, error):
        self.outcome = outcome
        self.message = message
        self.expected = expected
        self.actual = actual
        self.error = error


def assert_equal(test_case, actual, expected, message):
    try:
        assert actual == expected
        test_case.add_assert_result('PASSED', message, actual, expected, None)
    except AssertionError:
        test_case.add_assert_result('FAILED', message, actual, expected, print_error(traceback.format_exc()))
        raise AssertionError


def assert_true(test_case, actual, message):
    assert_equal(test_case, actual, True, message)


def assert_false(test_case, actual, message):
    assert_equal(test_case, actual, False, message)
