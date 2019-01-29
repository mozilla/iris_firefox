# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import os
from iris.api.core.util.parse_args import parse_args

logger = logging.getLogger(__name__)


def print_report_footer(platform, fx_version, fx_build, passed, failed,
                        skipped, errors, total_time, failures=None, blocked=None):
    """
    :param platform: Platform to be printed in the report footer.
    :param fx_version: Firefox version to be printed in the report footer.
    :param fx_build: Firefox build to be printed in the report footer.
    :param passed: Number of passed test cases.
    :param failed: Number of failed test cases.
    :param skipped: Number of skipped test cases.
    :param blocked: Number of blocked test cases
    :param errors: Number of test cases that run into errors.
    :param total_time: Time elapsed for a full run.
    :param failures: Test failures list.
    :return: Test results to be printed.
    """
    total = passed + failed + skipped + errors
    fx_details = 'Platform: %s, Firefox Version: %s, Firefox Build: %s' % (platform, fx_version, fx_build)
    test_results_str = 'Passed: %s, Failed: %s, Skipped: %s (Blocked: %s), Errors: %s -- Total: %s' \
                       % (passed, failed, skipped, len(blocked), errors, total)
    total_time_str = 'Total time: %s second(s)' % total_time

    failure_str = ''
    if len(failures):
        failure_str = '\n\nThe following tests did not pass:\n'
        for module in failures:
            failure_str += module + '\n'
        failure_str += '\n'

    separator = '\n' + '-' * 120 + '\n'
    test_results = (separator + fx_details + '\n' + test_results_str + ' ' *
                    (120 - (len(test_results_str) + len(total_time_str))) +
                    total_time_str + failure_str + separator)
    logger.info(test_results)
    return test_results


def format_outcome(outcome):
    """
    :param outcome: Test case resolution used to log the result.
    :return: String test case resolution('PASSED'/'FAILED').
    """
    if outcome:
        return 'PASSED'
    else:
        return 'FAILED'


def print_error(error):
    """
    :param error: Error message.
    :return: Formatted error message.
    """
    lines = error.splitlines()
    result = '\n'
    max_len = 0
    for line in lines:
        if len(line) > max_len:
            max_len = len(line)
    result = result + '-' * (max_len + 6) + '\n'
    for line in lines:
        result = result + '>> ' + line + ' ' * (max_len - len(line)) + ' <<' + '\n'
    result = result + '-' * (max_len + 6) + '\n'
    return result


def format_stack(stack):
    """
    :param stack: Stack trace error.
    :return: Formatted stack trace error.
    """
    result = 'Traceback (most recent call last):\n'
    for line in stack:
        result += '  File "' + str(line[0]) + '", line ' + str(line[1]) + ', in ' + str(line[2]) + '\n    ' + \
                  str(line[3]) + '\n'
    return result


def get_duration(start_time, end_time):
    """
    :param start_time: Start time.
    :param end_time: End time.
    :return: Duration displayed with 2 decimals.
    """
    return round(end_time - start_time, 2)


def print_results(current_test, test_case):
    """
    :param current_test: Test case(current) for which additional information will be printed.
    :param test_case: Instance of BaseTest class.
    :return: None.
    """
    logger.info('[%s] - >>> %s <<< (Finished in %s second(s))\n' % (
        current_test, test_case.outcome, get_duration(test_case.start_time, test_case.end_time)))


def write_test_failures(failures, master_test_list):
    master_run_directory = os.path.join(parse_args().workdir, 'runs')
    path = os.path.join(master_run_directory, 'last_fail.txt')

    if len(failures):
        if os.path.exists(path):
            os.remove(path)
        last_fail = open(path, 'w')
        for item in failures:
            for package in master_test_list:
                for test in master_test_list[package]:
                    if test["name"] == item:
                        last_fail.write(test["module"] + '\n')
        last_fail.close()
