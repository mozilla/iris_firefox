# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import ast

from moziris.configuration.config_parser import get_config_property






class TestRailTests:

    def __init__(self, test_case_name: str, suite_id: int, blocked_by: int, test_case_id: int,
                 outcome):

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
        self.outcome = outcome

    def get_test_status(self):
        """

        Parser for test_steps_assertion

        :return test_status

        """
        return self.outcome


    def get_test_case_name(self):
        """
        Method that will retrieve the test case_name

        :return test_case_name

        """
        return self.test_case_name

    def get_test_case_id(self):
        """
        Method that will retrieve the test case_id

        :return test_case_id

        """
        return self.test_case_id


class TestSuiteMap:
    suite_dictionary = ast.literal_eval(get_config_property("Test_rail", "suite_dictionary"))

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
        """
        Method that will parse config.ini and retrieve the suite name from
        suite_dictionary

        """
        for key in self.suite_dictionary:
            if self.suite_id == self.suite_dictionary.get(key):
                self.suite_name = key
