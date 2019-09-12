# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import logging


logger = logging.getLogger(__name__)


class TestResult(object):

    def __init__(self, item, node_name, outcome, message, actual, expected, file_name, error, line, traceback, test_duration):
        self.item = item
        self.node_name = node_name
        self.outcome = outcome
        self.message = message
        self.expected = expected
        self.actual = actual
        self.file_name = file_name
        self.error = error
        self.line = line
        self.traceback = traceback
        self.test_duration = test_duration


def create_result_object(assert_instance: tuple, start_time, end_time):
    """
    :param assert_instance: Assert object and test status
    :param start_time: Test Start Time
    :param end_time:Test End Time
    :return: Test_Result object
    """
    result = None
    outcome = assert_instance.__getitem__(1)

    if outcome == 'FAILED' or outcome == 'ERROR':
        assert_object = assert_instance.__getitem__(2)
        assert_info = normalize_assert(assert_object)
        result = TestResult(assert_instance.__getitem__(0), assert_info.get('node_name'), assert_instance.__getitem__(1),
                            assert_info.get('message'), assert_info.get('actual'), assert_info.get('expected'),
                            str(assert_instance.__getitem__(0).__dict__.get('fspath')),
                            assert_info.get('error'), assert_info.get('line'),
                            '\n  '.join(map(str, ['Traceback (most recent call last):'] + assert_instance.__getitem__(3)
                                            + ['%s: %s' % (assert_info.get('error'), assert_info.get('message'))])),
                            end_time - start_time)
    elif outcome == 'PASSED':
        test_item = assert_instance.__getitem__(0).__dict__
        result = TestResult(assert_instance.__getitem__(0), test_item.get('fspath'),
                            assert_instance.__getitem__(1), None, None, None, None,
                            None, None, None, end_time - start_time)
    elif outcome == 'SKIPPED':
        test_item = assert_instance.__getitem__(0).__dict__
        result = TestResult(assert_instance.__getitem__(0), test_item.get('fspath'),
                            assert_instance.__getitem__(1), None, None, None, None,
                            None, None, None, end_time - start_time)
    return result


def normalize_assert(assert_object):
    """
    :param assert_object:raw representation of assert details
    :return:result_map  ict

    """
    keys = ['node_name', 'line', 'error', 'message']

    # The assert string can be split using a colon, but on Windows, it can be a problem,
    # since file paths can begin with 'C:'. To work around this, we can split the string
    # using a colon AND a space.
    # However, we want to separate the line number from the file name, which has a colon,
    # but no space.
    # The solution is to insert a space after the file extension, and then split by colon/space.

    assert_object = str(assert_object).replace('.py:', '.py: ')
    values = assert_object.split(': ')

    result_map = {k: v for k, v in zip(keys, values)}
    try:

        if result_map.get('error') == AssertionError:

            if assert_object.__dict__.get('_excinfo')[1] is not None:
                extra_assert_info = assert_object.__dict__.get('_excinfo')[1]

            expected = {'expected': str(extra_assert_info).split('-')[1].split('\n')[0]}
            actual = {'actual': str(extra_assert_info).split('-')[1].split('+')[1]}

            result_map.update(actual)
            result_map.update(expected)

    except AssertionError as e:
        raise e

    return result_map
