# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import logging
import os
import time

import pytest

from src.core.api.os_helpers import OSHelper
from src.core.util.arg_parser import get_core_args
from src.core.util.json_utils import update_run_index, create_run_log
from src.core.util.run_report import create_footer
from src.core.util.test_assert import create_result_object
from src.email_report.email_client import submit_email_report

core_args = get_core_args()
logger = logging.getLogger(__name__)


class BaseTarget:
    completed_tests = []
    values = {}

    def __init__(self):
        self.args = self.get_target_args()
        self.target_name = 'Default target'
        self.cc_settings = [
            {'name': 'locale', 'type': 'list', 'label': 'Locale', 'value': OSHelper.LOCALES, 'default': 'en-US'},
            {'name': 'mouse', 'type': 'list', 'label': 'Mouse speed', 'value': ['0.0', '0.5', '1.0', '2.0'],
             'default': '0.5'},
            {'name': 'highlight', 'type': 'checkbox', 'label': 'Debug using highlighting'},
            {'name': 'override', 'type': 'checkbox', 'label': 'Run disabled tests'}
        ]

    def get_target_args(self):
        parser = argparse.ArgumentParser(description='Target-specific arguments', prog='iris')
        return parser.parse_known_args()[0]

    def pytest_sessionstart(self, session):
        """Called after the 'Session' object has been created and before performing test collection.

        :param _pytest.main.Session session: the pytest session object.
        """
        self.start_time = time.time()
        logger.info('\n' + 'Test session {} started'.format(session.name).center(os.get_terminal_size().columns, '-'))

        core_settings_list = []
        for arg in vars(core_args):
            core_settings_list.append('{}: {}'.format(arg, getattr(core_args, arg)))
        logger.info('\nIris settings:\n' + ', '.join(core_settings_list))

        application_settings_list = []

        for arg in vars(self.args):
            application_settings_list.append('{}: {}'.format(arg, getattr(self.args, arg)))
        logger.info(('\n{} settings:\n' +
                     ', '.join(application_settings_list)).format(str(core_args.application).capitalize()))
        update_run_index(self, False)

    def pytest_sessionfinish(self, session):
        """ called after whole test run finished, right before returning the exit status to the system.

        :param _pytest.main.Session session: the pytest session object.
        :param int exitstatus: the status which pytest will return to the system.
        """
        self.end_time = time.time()

        update_run_index(self, True)
        footer = create_footer(self)
        result = footer.print_report_footer()
        create_run_log(self)

        logger.info('\n' + 'Test session {} complete'.format(session.name).center(os.get_terminal_size().columns, '-'))

        if core_args.email:
            submit_email_report(self, result)

    def pytest_runtest_setup(self, item):
        os.environ['CURRENT_TEST'] = str(item.__dict__.get('fspath'))

    def pytest_runtest_teardown(self, item):
        pass

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
            @staticmethod
            def get(name):
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

            if str(item.__dict__.get('fspath')) in str(call.excinfo):
                logger.debug('Test failed with assert')
                outcome = "FAILED"
            else:
                logger.debug('Test failed with error')
                outcome = "ERROR"

            assert_object = (item, outcome, call.excinfo)

            test_result = create_result_object(assert_object, call.start, call.stop)

            self.completed_tests.append(test_result)

        elif call.when == "call" and call.excinfo is None:
            outcome = 'PASSED'
            test_instance = (item, outcome, None)

            test_result = create_result_object(test_instance, call.start, call.stop)

            self.completed_tests.append(test_result)

        elif call.when == "setup" and item._skipped_by_mark:
            outcome = 'SKIPPED'
            test_instance = (item, outcome, None)

            test_result = create_result_object(test_instance, call.start, call.stop)

            self.completed_tests.append(test_result)


def reason_for_failure(report):
    if report.outcome == 'passed':
        return ''
    else:
        return report.longreprtext
