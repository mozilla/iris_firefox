# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import ast

from iris.api.helpers.general import get_config_property


class TestRailTests(object):
    test_status = ''
    test_steps = []

    def __init__(self, test_case_name, suite_id, blocked_by, test_case_id, test_steps_assertion):

        """
        :param test_case_name: name of the test case
        :param suite_id: TestRail suite id
        :param test_case_id: TestRail test case id
        :param test_steps_assertion:  collection of test assertions
        """
        self.test_case_name = test_case_name
        self.section_id = suite_id
        self.blocked_by = blocked_by
        self.test_case_id = test_case_id
        self.test_case_steps = test_steps_assertion

    def get_test_status(self):
        for assertion in range(len(self.test_case_steps)):
            if self.test_case_steps[assertion].outcome == 'PASSED':
                self.test_status = 'PASSED'
            else:
                self.test_status = 'FAILED'
                break
        return self.test_status

    def get_steps_results(self):
        for message in range(len(self.test_case_steps)):
            test_step = self.test_case_steps[message].message
            self.test_steps.append(test_step)
        return self.test_steps

    def get_test_case_name(self):
        return self.test_case_name

    def get_test_case_id(self):
        return self.test_case_id


class TestSuiteMap:
    suite_dictionary = ast.literal_eval(get_config_property("Test_Rail_Suites", "suite_dictionary"))

    suite_name = ''

    def __init__(self, suite_id, test_results_list):

        """

        :param suite_id: TestRail suite id
        :param test_results_list: a list of TestRailTests objects
        """
        self.suite_id = suite_id
        self.test_results_list = test_results_list
        self.get_suite_name()

    def get_suite_name(self):
        for key in self.suite_dictionary:
            if self.suite_id == self.suite_dictionary.get(key):
                self.suite_name = key
