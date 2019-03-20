# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from src.configuration.config_parser import logger
from src.core.api.os_helpers import OSHelper
from src.core.util.test_assert import TestResult


class ReportFooter(object):

    def __init__(self, app, total_tests_run, passed_tests, failed_tests, skipped_tests, error_tests, total_duration, failures):
        self.platform = OSHelper.get_os().value
        self.app = app
        self.total_tests_run = total_tests_run
        self.failed_tests = failed_tests
        self.passed_tests = passed_tests
        self.skipped_tests = skipped_tests
        self.error_tests = error_tests
        self.total_duration = total_duration
        self.failures = failures

    def print_report_footer(self):
        total = self.passed_tests + self.failed_tests + self.skipped_tests + self.error_tests
        separator = '\n' + '-' * 120 + '\n'
        failure_str = ''

        if self.failures.__len__() is not None:
            failure_str = '\n\nThe following tests did not pass:\n'
            for failed_tests in self.failures:
                failure_str += failed_tests + '\n'
                failure_str += '\n'

        app_details = 'Application: %s,Platform: %s' % (self.app.target_name, self.platform)
        test_results_str = 'Passed: %s, Failed: %s, Skipped: %s, Errors %s   -- Total: %s' \
                           % (self.passed_tests, self.failed_tests, self.skipped_tests, self.error_tests, total)
        total_time_str = 'Total time: %s second(s)' % self.total_duration

        test_results = (separator + app_details + '\n' + test_results_str + ' ' *
                        (120 - (len(test_results_str) + len(total_time_str))) +
                        total_time_str + failure_str + separator)

        logger.info(test_results)
        return test_results


def create_footer(app):
    """

    :param app: Target Application Ex:Notepad,Firefox
    :return: ReportFooter object
    """
    skipped = 0
    failed = 0
    passed = 0
    errors = 0
    total_duration = 0

    failed_tests = []

    for test in app.completed_tests:

        if test.outcome == 'FAILED':
            failed = failed + 1
            failed_tests.append(test.file_name)
        elif test.outcome == 'PASSED':
            passed = passed + 1
        elif test.outcome == 'SKIPPED':
            skipped = skipped + 1
        elif test.outcome == 'ERROR':
            failed_tests.append(test.file_name)
            errors = errors + 1

        total_duration = total_duration + test.test_duration

    return ReportFooter(app, passed + skipped + failed + errors, passed, failed, skipped, errors, total_duration, failed_tests)
