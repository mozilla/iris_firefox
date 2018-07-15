from datetime import date
import api_client
from iris.api.core.settings import *
from iris.asserts import *
from iris.testrail.test_case_results import *
import ast
from iris.api.core.errors import *

logger = logging.getLogger(__name__)


class TestRail:
    project_name = 'Firefox Desktop'
    run_name = ''

    def __init__(self):

        logger.info('----STARTING TEST_RAIL REPORTING-------')

        # Set the TestRail URL
        # TestRail UserName and Password
        self.test_rail_url = get_credential('Test_rail', 'test_rail_url')
        self.client = api_client.APIClient(self.test_rail_url)
        self.client.user = get_credential('Test_rail', 'username')
        self.client.password = get_credential('Test_rail', 'password')

    def get_all_projects(self):

        # retrieve all projects from testRail

        try:
            projects = self.client.send_get('get_projects')
        except Exception:
            raise TestRailError("No projects found")
        return projects

    def get_project_id(self, project_name):

        # retrieve project from testRail based on projectName

        project_id = None
        projects = self.get_all_projects()
        for project in projects:
            if project['name'] == project_name:
                project_id = project['id']
                break
            else:
                continue
        return project_id

    def get_all_runs(self, project_name):

        # retrieve all runs from a specific projects

        project_id = self.get_project_id(project_name)
        try:
            test_runs = self.client.send_get('get_runs/%s' % project_id)
        except Exception:
            raise TestRailError('Error!! no runs found in this specific project %s', project_name)
        else:
            return test_runs

    # return a specific run id based on project name

    def get_specific_run_id(self, project_name, test_run_name):
        test_runs = self.get_all_runs(project_name)
        for test_run in test_runs:
            if test_run['name'] == test_run_name:
                run_id = test_run['id']
                return run_id
            else:
                logger.error('Test run not found with name %s', test_run_name)

    # get all tests from a specific run

    def get_tests_from_run(self, project_name, test_run_name):
        run_id = self.get_specific_run_id(project_name, test_run_name)
        try:
            tests = self.client.send_get('get_tests/' + str(run_id))
        except Exception:
            raise TestRailError('Error no runs found in this specific project')
        return tests

    def create_test_plan(self, build_id, firefox_version, test_case_object_list):

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
            raise TestRailError('Failed to create Test Rail Test Plan ')

        else:
            logger.info('TEST plan %s was successfully created and ' % self.run_name)
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
                raise TestRailError('Invalid Api Response format')

            self.add_test_results(test_run_list, suite_runs)

    def add_test_results(self, test_run_list, suite_runs):

        # status_id = 1 for Passed,
        # status_id  = 5 for Failed
        # status_id  = 2 for Blocked--need to add logic for blocked

        for run in test_run_list:
            if isinstance(run, dict):
                run_id = run.get('id')
            for suite in suite_runs:
                object_list = []
                results = {}
                if isinstance(suite, TestSuiteMap):
                    if suite.suite_name in run.get('name'):
                        suite_id_tests = suite.test_results_list
                        for test in suite_id_tests:
                            if isinstance(test, TestRailTests):
                                payload = {}
                                complete_test_assert = ''
                                test_results = test.get_test_status()
                                test_results_steps = test.test_case_steps
                            for iterator in range(len(test_results_steps)):
                                test_steps = ' *Test assertion:* \n  ' + str(
                                    test_results_steps[
                                        iterator].message) + ' \n - Expected: ' + str(
                                    test_results_steps[iterator].expected) + ' \n - Actual: ' + str(
                                    test_results_steps[iterator].actual)
                                complete_test_assert = test_steps + '\n\n\n' + complete_test_assert

                            if test_results.__contains__('FAILED') or test_results.__contains__('ERROR'):
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
                                raise TestRailError('Failed to Update TestRail run  %s ', run.get('name'))

                            else:
                                logger.info('Successfully added test results in test run name: %s\n ' % run.get('name'))

    @staticmethod
    def generate_test_plan_name(firefox_version):

        # name of the test run is generated based on the OS , date and build number
        # this method can be be improved to add more details

        # noinspection PyPep8
        run_name = (
            '[' + 'Firefox ' + firefox_version + ']' + '[' + Settings.getOS().capitalize() + ']'
            + 'Iris Test Run ' + str(date.today()))
        return run_name

    @staticmethod
    def generate_run_description(firefox_build_id, firefox_version):

        # the result of this method will populate the 'description' of the test run
        # current implementation will display only build information but can be enhanced to

        return '**BUILD INFORMATION**' + '\n' + '*Firefox Build ID*:' + str(
            firefox_build_id) + '\n' + '*Firefox Version:*' + firefox_version

    @staticmethod
    def generate_test_suite_collection_objects(test_rail_tests):

        # the test results collected at run are mapped in a new object TestSuiteMap and grouped on suite Id's

        test_suite_array = []
        suite_dictionary = ast.literal_eval(get_credential('Test_Rail_Suites', 'suite_dictionary'))
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
