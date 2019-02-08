# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


class TestResult(object):

    def __init__(self, node_name, outcome, message, actual, expected, error, line, test_duration):
        self.node_name = node_name
        self.outcome = outcome
        self.message = message
        self.expected = expected
        self.actual = actual
        self.error = error
        self.line = line
        self.test_duration = test_duration


def create_result_object(assert_instance: tuple, start_time, end_time):
    """
    :param assert_instance: Assert object and test status
    :param start_time: Test Start Time
    :param end_time:Test End Time
    :return: Test_Result object
    """

    if assert_instance.__getitem__(1) == "FAILED":
        assert_object = assert_instance.__getitem__(0)
        assert_info = normalize_assert(assert_object)

        result = TestResult(assert_info.get('node_name'), assert_instance.__getitem__(1), assert_info.get('message'),
                            assert_info.get('actual'), assert_info.get('expected'),
                            assert_info.get("error"), assert_info.get("line"), end_time - start_time)
    elif assert_instance.__getitem__(1) == "PASSED":

        test_item = assert_instance.__getitem__(0).__dict__

        result = TestResult(test_item.get('fspath'), assert_instance.__getitem__(1), None,
                            None, None,
                            None, None, end_time - start_time)
    elif assert_instance.__getitem__(1) == "SKIPPED":
        test_item = assert_instance.__getitem__(0).__dict__

        result = TestResult(test_item.get('fspath'), assert_instance.__getitem__(1), None,
                            None, None,
                            None, None, end_time - start_time)

    return result


def normalize_assert(assert_object):
    """
    :param assert_object:raw representation of assert details
    :return:result_map  ict

    """

    keys = ['node_name', "line", "error", "message"]
    values = str(assert_object).split(':')

    result_map = {k: v for k, v in zip(keys, values)}
    if assert_object.__dict__.get('_excinfo')[1] is not None:
        extra_assert_info = assert_object.__dict__.get('_excinfo')[1]

        expected = {'expected': str(extra_assert_info).split('-')[1].split('\n')[0]}
        actual = {'actual': str(extra_assert_info).split('-')[1].split('+')[1]}

        result_map.update(actual)
        result_map.update(expected)

    return result_map
