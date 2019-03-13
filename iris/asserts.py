# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import traceback

from api.helpers.results import *

class Result(object):

    def __init__(self, outcome, message, actual, expected, error):
        self.outcome = outcome
        self.message = message
        self.expected = expected
        self.actual = actual
        self.error = error


def assert_equal(test_case, actual, expected, message):
    """
    :param test_case: Instance of BaseTest class.
    :param actual: Actual result.
    :param expected: Expected result.
    :param message: Text message.
    :return: None.
    """
    try:
        assert actual == expected
        test_case.add_results(Result('PASSED', message, actual, expected, None))
    except AssertionError:
        test_case.add_results(
            Result('FAILED', message, actual, expected, print_error(format_stack(traceback.extract_stack()))))
        raise AssertionError


def assert_contains(test_case, actual, expected, message):
    """
    :param test_case: Instance of BaseTest class.
    :param actual: Actual result.
    :param expected: Expected result.
    :param message: Text message.
    :return: None.
    """
    try:
        assert expected in actual
        test_case.add_results(Result('PASSED', message, actual, expected, None))
    except AssertionError:
        test_case.add_results(
            Result('FAILED', message, actual, expected, print_error(format_stack(traceback.extract_stack()))))
        raise AssertionError


def assert_not_equal(test_case, actual, expected, message):
    """
    :param test_case: Instance of BaseTest class.
    :param actual: Actual result.
    :param expected: Expected result.
    :param message: Text message.
    :return: None.
    """
    try:
        assert actual != expected
        test_case.add_results(Result('PASSED', message, actual, expected, None))
    except AssertionError:
        test_case.add_results(
            Result('FAILED', message, actual, expected, print_error(format_stack(traceback.extract_stack()))))
        raise AssertionError


def assert_true(test_case, actual, message):
    """Call the assert_equal() method with expected result TRUE.

    :param test_case: Instance of BaseTest class.
    :param actual: Actual result.
    :param message: Text message.
    :return: None.
    """
    assert_equal(test_case, actual, True, message)


def assert_false(test_case, actual, message):
    """Call the assert_equal() method with expected result FALSE.

    :param test_case: Instance of BaseTest class.
    :param actual: Actual result.
    :param message: Text message.
    :return: None.
    """
    assert_equal(test_case, actual, False, message)
