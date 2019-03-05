# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from targets.firefox.parse_args import parse_args
from src.core.util.json_utils import update_run_index
from src.core.util.test_assert import create_result_object
from src.core.util.run_report import create_footer
from targets.firefox.firefox_app.fx_collection import FX_Collection
from targets.firefox.firefox_app.fx_browser import FirefoxApp

args = parse_args()


class BaseTarget:

    completed_tests = []

    def __init__(self):
        self.target_name = 'Default target'
        self.cc_settings = []
        self.locale = args.locale

    def pytest_sessionstart(self, session):
        """Called after the 'Session' object has been created and before performing test collection.

        :param _pytest.main.Session session: the pytest session object.
        """
        print('\n\n** Test session {} started **\n'.format(session.name))
        print('\nIris settings: \n')

        settings_list = []

        for arg in vars(args):
            settings_list.append('{}: {}'.format(arg, getattr(args, arg)))
        print(', '.join(settings_list))
        print('\n')
        update_run_index(self, False)


    def pytest_sessionfinish(self, session):
        """ called after whole test run finished, right before returning the exit status to the system.

        :param _pytest.main.Session session: the pytest session object.
        :param int exitstatus: the status which pytest will return to the system.
        """

        update_run_index(self, True)
        footer = create_footer(self)
        footer.print_report_footer()

        print("\n\n** Test session {} complete **\n".format(session.name))

    def pytest_runtestloop(self, session):
        pass

    def pytest_runtest_logstart(self, nodeid, location):
        pass

    def pytest_runtest_call(self, item):
        pass

    def pytest_runtest_logfinish(self, nodeid, location):
        pass

    @pytest.fixture
    def option(self, pytestconfig):
        """
        fixture for ovewriting values in pytest.ini file

        :return: Option Object
        """

        new_value = {}

        class Options:

            def get(self, name):
                return new_value.get(name, pytestconfig.getini(name))

        return Options()

    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_makereport(self, item, call):

        """ return a :py:class:`_pytest.runner.TestReport` object
            for the given :py:class:`pytest.Item <_pytest.main.Item>` and
            :py:class:`_pytest.runner.CallInfo`.

            Stops at first non-None result
            """

        if call.when == "call" and call.excinfo is not None:

            outcome = "FAILED"
            assert_object = (call.excinfo, outcome)

            test_result = create_result_object(assert_object, call.start, call.stop)

            self.completed_tests.append(test_result)

        elif call.when == "call" and call.excinfo is None:
            outcome = 'PASSED'
            test_instance = (item, outcome)

            test_result = create_result_object(test_instance, call.start, call.stop)

            self.completed_tests.append(test_result)

        elif call.when == "setup" and item._skipped_by_mark:
            outcome = 'SKIPPED'
            test_instance = (item, outcome)

            test_result = create_result_object(test_instance, call.start, call.stop)

            self.completed_tests.append(test_result)


def reason_for_failure(report):
    if report.outcome == 'passed':
        return ''
    else:
        return report.longreprtext
