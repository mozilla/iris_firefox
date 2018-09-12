# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import api_client
from datetime import date

from iris.api.core.settings import *
from iris.asserts import *
from iris.test_rail.test_case_results import *
from iris.api.core.errors import *

logger = logging.getLogger(__name__)


class TestRail:
    project_name = 'Firefox Desktop'
    run_name = ''

    def __init__(self):
        logger.info('Starting TestRail reporting.')

        # Set the Test_Rail URL, user name and password.
        self.test_rail_url = get_config_property('Test_rail', 'test_rail_url')
        self.client = api_client.APIClient(self.test_rail_url)
        self.client.user = get_config_property('Test_rail', 'username')
        self.client.password = get_config_property('Test_rail', 'password')

    # Retrieve all projects from Test_Rail.

    def get_all_projects(self):
        try:
            projects = self.client.send_get('get_projects')
        except Exception:
            raise TestRailError("No projects found")
        return projects

    # Retrieve project from Test_Rail based on project name.

    def get_project_id(self, project_name):

        """
        :param project_name:  name of TestRail Project (Ex. Firefox Desktop)
        :return: Id of the Project
        """

        project_id = None
        projects = self.get_all_projects()
        for project in projects:
            if project['name'] == project_name:
                project_id = project['id']
                break
            else:
                continue
        return project_id

    # Retrieve all runs from a specific project.

    def get_all_runs(self, project_name):

        """
        :param project_name: name of TestRail Project (Ex. Firefox Desktop)
        :return: a list of test runs from a project
        """

        project_id = self.get_project_id(project_name)
        try:
            test_runs = self.client.send_get('get_runs/%s' % project_id)
        except Exception:
            raise TestRailError('Error: no runs found in this specific project %s', project_name)
        else:
            return test_runs

    # Return a specific run id based on project name.

    def get_specific_run_id(self, project_name, test_run_name):

        """
        :param project_name:  name of TestRail Project (Ex. Firefox Desktop)
        :param test_run_name:  name of TestRail test run (Bx. Bookmarks, History)
        :return: Id of the Test Run (Ex 17,34)
        """
        test_runs = self.get_all_runs(project_name)
        for test_run in test_runs:
            if test_run['name'] == test_run_name:
                run_id = test_run['id']
                return run_id
            else:
                logger.error('Test run not found: %s', test_run_name)

    # Get all tests from a specific run.

    def get_tests_from_run(self, project_name, test_run_name):

        """
        :param project_name: name of TestRail Project (Ex. Firefox Desktop)
        :param test_run_name: name of TestRail test run (Ex. Bookmarks, History)
        :return: a list of test cases from a specific test run
        """

        run_id = self.get_specific_run_id(project_name, test_run_name)
        try:
            tests = self.client.send_get('get_tests/' + str(run_id))
        except Exception:
            raise TestRailError('Error: no runs found in this specific project')
        return tests

    def create_test_plan(self, build_id, firefox_version, test_case_object_list):

        """
        Creates a Test Plan and Test Run for all suites that are mapped in a project.

        :param build_id:  firefox_build (Ex 20180704003137)
        :param firefox_version: actual version of Firefox (Ex 61.03)
        :param test_case_object_list: a list of TestRailTests objects
        :return: None
        """

        self.run_name = self.generate_test_plan_name(firefox_version)
        data_array = []
        payload = {}
        suite_runs = self.generate_test_suite_collection_objects(test_case_object_list)
        for suite in suite_runs:
            data = {}
            test_case_ids = []
            data['suite_id'] = suite.suite_id
            data['name'] = suite.suite_name
            data['include_all'] = False
            for test_case in suite.test_results_list:
                if isinstance(suite, TestSuiteMap):
                    if isinstance(test_case, TestRailTests):
                        case_id = test_case.test_case_id
                        test_case_ids.append(case_id)
            data['case_ids'] = test_case_ids
            data_array.append(data)

        payload['name'] = self.run_name
        payload['entries'] = data_array
        payload['description'] = self.generate_run_description(build_id, firefox_version)

        project_id = self.get_project_id(self.project_name)

        try:
            test_plan_api_response = self.client.send_post('add_plan/%s' % project_id, payload)
        except Exception:
            raise TestRailError('Failed to create Test Rail Test Plan')

        else:
            logger.info('Test plan %s was successfully created' % self.run_name)
            entries_list = test_plan_api_response.get('entries')
            test_run_list = []
            if isinstance(entries_list, list):
                for test_run_entry in entries_list:
                    run = test_run_entry
                    if isinstance(run, dict):
                        run_object_list = run.get('runs')
                        if isinstance(run_object_list, list):
                            for run_object in run_object_list:
                                test_run = run_object
                                test_run_list.append(test_run)
                        else:
                            raise TestRailError('Invalid object format')
                    else:
                        raise TestRailError('Invalid object format')
            else:
                raise TestRailError('Invalid API Response format')

            self.add_test_results(test_run_list, suite_runs)

    def add_test_results(self, test_run_list, suite_runs):

        """
        :param test_run_list: a list of runs that were generated in the test plan creation
        :param suite_runs: a list of suite objects
        :return: None

        status_id = 1 for Passed
        status_id = 5 for Failed
        status_id = 2 for Blocked
        """

        for run in test_run_list:
            if isinstance(run, dict):
                run_id = run.get('id')
            else:
                logger.error('Invalid API response.')
                break
            for suite in suite_runs:
                object_list = []
                results = {}
                if isinstance(suite, TestSuiteMap):
                    if suite.suite_name in run.get('name'):
                        suite_id_tests = suite.test_results_list
                        for test in suite_id_tests:
                            payload = {}
                            complete_test_assert = ''
                            test_results = test.get_test_status()
                            test_results_steps = test.test_case_steps
                            for iterator in range(len(test_results_steps)):
                                message = test_results_steps[iterator].message
                                expected = test_results_steps[iterator].expected
                                actual = test_results_steps[iterator].actual
                                test_steps = ' *Test assertion:* \n  %s \n - Expected: %s \n - Actual: %s' % (
                                    message, expected, actual)
                                complete_test_assert = test_steps + '\n\n\n' + complete_test_assert

                            if len(test.blocked_by) > 1:
                                payload['status_id'] = 2
                                payload['defects'] = test.blocked_by
                            elif test_results.__contains__('FAILED') or test_results.__contains__('ERROR'):
                                payload['status_id'] = 5
                            else:
                                payload['status_id'] = 1
                            payload['comment'] = complete_test_assert
                            payload['case_id'] = test.test_case_id
                            object_list.append(payload)
                            results['results'] = object_list

                        if run_id is not None:
                            try:
                                self.client.send_post('add_results_for_cases/%s' % run_id, results)
                            except Exception:
                                raise TestRailError('Failed to Update Test_Rail run %s', run.get('name'))

                            else:
                                logger.info(
                                    'Successfully added test results in test run name: %s' % run.get('name'))
                        else:
                            raise TestRailError('Invalid run_id')
                    else:
                        continue
                else:
                    raise TestRailError('Invalid API Response')

    @staticmethod
    def generate_test_plan_name(firefox_version):

        """
        :param firefox_version: actual version of Firefox
        :return: name of the test plan

        name of the test run is generated based on the OS , date and build number
        this method can be be improved to add more details
        """

        # noinspection PyPep8
        test_plan_name = '[Firefox %s][%s]Iris Test Run %s' % (
            firefox_version, Settings.get_os().capitalize(), date.today())
        return test_plan_name

    @staticmethod
    def generate_run_description(firefox_build_id, firefox_version):

        """
        :param firefox_build_id: firefox_build (Ex 20180704003137)
        :param firefox_version: actual version of Firefox (Ex 61.03)
        :return: a string that contain basic firefox build info's
        """

        run_desc = '**BUILD INFORMATION**\n*Firefox Build ID*:%s\n*Firefox Version:*%s' % (
            firefox_build_id, firefox_version)
        return run_desc

    @staticmethod
    def generate_test_suite_collection_objects(test_rail_tests):

        """
        :param test_rail_tests: a list of TestRailTest
        :return: a list of TestSuiteMap
        """

        test_suite_array = []
        suite_dictionary = ast.literal_eval(get_config_property('Test_Rail_Suites', 'suite_dictionary'))
        suite_ids = []
        for suite in suite_dictionary:
            suite_ids.append(suite_dictionary.get(suite))
        for suite_id in suite_ids:
            test_case_ids = []
            for test_result in test_rail_tests:
                if isinstance(test_result, TestRailTests):
                    if suite_id == test_result.section_id:
                        test_case_ids.append(test_result)
            if not test_case_ids:
                continue
            else:
                test_suite_object = TestSuiteMap(suite_id, test_case_ids)
                test_suite_array.append(test_suite_object)

        return test_suite_array
