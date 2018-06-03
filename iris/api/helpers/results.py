# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
import logging

logger = logging.getLogger(__name__)


def print_report_footer(platform, fx_version, fx_build, passed, failed,
                        skipped, errors, total_time, failures=None):
    total = passed + failed + skipped + errors
    fx_details = 'Platform: %s, Firefox Version: %s, Firefox Build: %s' % (platform, fx_version, fx_build)
    test_results_str = 'Passed: %s, Failed: %s, Skipped: %s, Errors: %s -- Total: %s' % (passed, failed, skipped,
                                                                                         errors, total)
    total_time_str = 'Total time: %s second(s)' % total_time

    failure_str = ''
    if len(failures):
        failure_str = '\n\nThe following tests did not pass:\n'
        for module in failures:
            failure_str += module + '\n'
        failure_str += '\n'

    separator = '\n' + '-' * 120 + '\n'
    logger.info(separator + fx_details + '\n' + test_results_str + ' ' *
                (120 - (len(test_results_str) + len(total_time_str))) +
                total_time_str + failure_str + separator)


def format_outcome(outcome):
    if outcome:
        return 'PASSED'
    else:
        return 'FAILED'


def print_error(error):
    lines = error.splitlines()
    result = '\n'
    max_len = 0
    for line in lines:
        if len(line) > max_len:
            max_len = len(line)
    result = result + '-' * (max_len + 4) + '\n'
    for line in lines:
        result = result + '» ' + line + ' ' * (max_len - len(line)) + ' «' + '\n'
    result = result + '-' * (max_len + 4) + '\n'
    return result


def format_stack(stack):
    result = 'Traceback (most recent call last):\n'
    for line in stack:
        result += '  File "' + str(line[0]) + '", line ' + str(line[1]) + ', in ' + str(line[2]) + '\n    ' + \
                  str(line[3]) + '\n'
    return result


def get_duration(start_time, end_time):
    return round(end_time - start_time, 2)


def print_results(current_test, test_case):
    for result in test_case.results:
        if 'ERROR' == result.outcome:
            logger.error('Error encountered in test, outcome: >>> ERROR <<< %s' % '\n' + result.error if
                         result.error else '')
        elif 'FAILED' == result.outcome:
            logger.warning('Step: %s, outcome: >>> %s <<< %s' % (
                result.message, result.outcome, '\n' + result.error if result.error else ''))
        elif 'PASSED' == result.outcome:
            logger.success('Step: %s, outcome: >>> %s <<<' % (result.message, result.outcome))
    logger.info('[%s] - >>> %s <<< (Finished in %s second(s))\n' % (
        current_test, test_case.outcome, get_duration(test_case.start_time, test_case.end_time)))
