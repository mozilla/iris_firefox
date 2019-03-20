# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
from multiprocessing import Process
import os

from src.base.target import *
from src.core.util.local_web_server import LocalWebServer
from src.core.util.path_manager import PathManager
from targets.firefox.firefox_ui.helpers.general import confirm_firefox_launch
from targets.firefox.firefox_ui.helpers.keyboard_shortcuts import maximize_window
from targets.firefox.parse_args import parse_args

# from targets.firefox.testrail.testcase_results import TestRailTests
from targets.firefox.bug_manager import *

logger = logging.getLogger(__name__)


class Target(BaseTarget):
    test_run_object_list = []

    def __init__(self):
        BaseTarget.__init__(self)
        self.target_name = 'Firefox'
        self.values = {'fx_version': 0, 'fx_build_id': 0, 'channel': '0'}

        self.cc_settings = [
            {'name': 'firefox', 'type': 'list', 'label': 'Firefox',
             'value': ['local', 'latest', 'latest-esr', 'latest-beta', 'nightly'], 'default': 'beta'},
            {'name': 'locale', 'type': 'list', 'label': 'Locale', 'value': ['en-US'], 'default': 'en-US'},
            {'name': 'mouse', 'type': 'list', 'label': 'Mouse speed', 'value': ['0.0', '0.5', '1.0', '2.0'],
             'default': '0.5'},
            {'name': 'highlight', 'type': 'checkbox', 'label': 'Debug using highlighting', 'value': False},
            {'name': 'override', 'type': 'checkbox', 'label': 'Run disabled tests', 'value': False},
            {'name': 'email', 'type': 'checkbox', 'label': 'Email results', 'value': False},
            {'name': 'report', 'type': 'checkbox', 'label': 'Create TestRail report', 'value': False}
        ]
        self.local_web_root = os.path.join(PathManager.get_module_dir(), 'targets', 'firefox', 'local_web')

    @pytest.fixture(scope="class", autouse=True)
    def use_firefox(self, request):

        fx = args.firefox
        locale = args.locale

        self.browser = FX_Collection.get(fx, locale)
        if not self.browser:
            FX_Collection.add(fx, locale)
            self.browser = FX_Collection.get(fx, locale)
        self.browser.start()
        self.values = {'fx_version': self.browser.version, 'fx_build_id': self.browser.build_id,
                       'channel': self.browser.channel}
        confirm_firefox_launch()
        maximize_window()

        def teardown():
            if self.browser.runner and self.browser.runner.process_handler:
                from targets.firefox.firefox_ui.helpers.keyboard_shortcuts import quit_firefox
                quit_firefox()
                status = self.browser.runner.process_handler.wait(15)
                if status is None:
                    self.browser.runner.stop()

        request.addfinalizer(teardown)

    # def _disable_catchlog(self,item):
    #     logger = logging.getLogger()
    #     if item.catch_log_handler in logger.handlers:
    #         logger.handlers.remove(item.catch_log_handler)

    def pytest_sessionstart(self, session):
        BaseTarget.pytest_sessionstart(self, session)
        try:
            port = parse_args().port
            self.process_list = []
            logger.info('Starting local web server on port %s for directory %s' % (port, self.local_web_root))
            web_server_process = Process(target=LocalWebServer, args=(self.local_web_root, port,))
            self.process_list.append(web_server_process)
            web_server_process.start()
        except IOError:
            logger.critical('Unable to launch local web server, aborting Iris.')
            # TODO: abort Iris

    def pytest_sessionfinish(self, session):
        BaseTarget.pytest_sessionfinish(self, session)
        for process in self.process_list:
            logger.info('Terminating process.')
            process.terminate()
            process.join()
        logger.debug('Finishing Firefox session')

    def pytest_runtest_setup(self, item):
        BaseTarget.pytest_runtest_setup(self, item)
        if item.name == 'test_run':
            values = item.own_markers[0].kwargs
            if 'exclude' in values and OSHelper.get_os().value == values.get('exclude'):
                logger.info(
                    'Test excluded: - [%s]: %s' % (
                        item._nodeid.split(':')[0], values.get('description')))
                test_instance = (item, 'SKIPPED', None)

                test_result = create_result_object(test_instance, 0, 0)
                self.completed_tests.append(test_result)
                pytest.skip(item)

            elif 'blocked_by' in values:
                bug_id = values.get('blocked_by')
                if is_blocked(bug_id):
                    logger.info(
                        'Test skipped: - [%s]: %s' % (
                            item._nodeid.split(':')[0], values.get('description')))
                    test_instance = (item, 'SKIPPED', None)

                    test_result = create_result_object(test_instance, 0, 0)
                    self.completed_tests.append(test_result)
                    pytest.skip(item)

    def pytest_runtest_call(self, item):
        """ called to execute the test ``item``. """

        logger.info(
            'Executing: - [%s]: %s' % (
                item._nodeid.split(':')[0], item.own_markers[0].kwargs.get('description')))

    # @pytest.hookimpl(hookwrapper=True, trylast=True)
    # def pytest_runtest_teardown(self,item):
    #     # self._disable_catchlog(item)
    #     # yield

    # @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    # def pytest_runtest_makereport(self, item, call):
    #     BaseTarget.pytest_runtest_makereport(self, item, call)
    #
    #     outcome = yield
    #     report = outcome.get_result()
    #
    #     if report.when == "call":
    #         test_case_instance = item.instance
    #         test_object_result = TestRailTests(test_case_instance.meta,
    #                                            test_case_instance.test_suite_id, test_case_instance.test_case_id,
    #                                            test_case_instance.blocked_by, test_case_instance.test_results)
    #
    #         self.test_run_object_list.append(test_object_result)

    # def pytest_runtest_call(self, item):
    # if hasattr(item.instance, 'fx'):
    #     fx = item.instance.fx
    # else:
    #     fx = parse_args().firefox
    #
    # if hasattr(item.instance, 'locale'):
    #     locale = item.instance.locale
    # else:
    #     locale = parse_args().locale

    # from targets.firefox.firefox_app.fx_collection import FX_Collection
    # if FX_Collection.get(fx, locale):
    #     print('Already installed')
    #     print(FX_Collection.get(fx, locale))
    # else:
    #     print('Firefox version: {}, locale: {} not found!'.format(fx, locale))
    #     FX_Collection.add(fx, locale)
    #     print(FX_Collection.get(fx, locale))
