# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
import os
from multiprocessing import Process

import pytest

from src.base.target import BaseTarget
from src.core.api.mouse.mouse import mouse_reset
from src.core.api.os_helpers import OSHelper
from src.core.util.arg_parser import get_core_args
from src.core.util.local_web_server import LocalWebServer
from src.core.util.path_manager import PathManager
from src.core.util.test_assert import create_result_object
from targets.firefox.bug_manager import is_blocked
from targets.firefox.firefox_app.fx_browser import FXRunner, FirefoxProfile, set_update_channel_pref
from targets.firefox.firefox_app.fx_collection import FX_Collection
from targets.firefox.parse_args import get_target_args
from targets.firefox.testrail.testrail_client import report_test_results

logger = logging.getLogger(__name__)
target_args = get_target_args()
core_args = get_core_args()


class Target(BaseTarget):
    test_run_object_list = []

    def __init__(self):
        BaseTarget.__init__(self)
        self.target_name = 'Firefox'

        self.process_list = []

        self.cc_settings = [
            {'name': 'firefox', 'type': 'list', 'label': 'Firefox',
             'value': ['local', 'latest', 'latest-esr', 'latest-beta', 'nightly'], 'default': 'beta'},
            {'name': 'locale', 'type': 'list', 'label': 'Locale', 'value': OSHelper.LOCALES, 'default': 'en-US'},
            {'name': 'mouse', 'type': 'list', 'label': 'Mouse speed', 'value': ['0.0', '0.5', '1.0', '2.0'],
             'default': '0.5'},
            {'name': 'highlight', 'type': 'checkbox', 'label': 'Debug using highlighting'},
            {'name': 'override', 'type': 'checkbox', 'label': 'Run disabled tests'},
            {'name': 'email', 'type': 'checkbox', 'label': 'Email results'},
            {'name': 'report', 'type': 'checkbox', 'label': 'Create TestRail report'}
        ]
        self.local_web_root = os.path.join(PathManager.get_module_dir(), 'targets', 'firefox', 'local_web')

    def pytest_sessionstart(self, session):
        BaseTarget.pytest_sessionstart(self, session)
        try:
            port = core_args.port

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
        if core_args.report:
            report_test_results(self)

    def pytest_runtest_setup(self, item):
        BaseTarget.pytest_runtest_setup(self, item)
        if not OSHelper.is_linux():
            mouse_reset()
        if item.name == 'test_run':
            values = item.own_markers[0].kwargs
            if 'exclude' in values and OSHelper.get_os() in values.get('exclude'):
                logger.info(
                    'Test excluded: - [%s]: %s' % (
                        item.nodeid.split(':')[0], values.get('description')))
                test_instance = (item, 'SKIPPED', None)

                test_result = create_result_object(test_instance, 0, 0)
                self.completed_tests.append(test_result)
                pytest.skip(item)

            elif 'blocked_by' in values:
                bug_id = values.get('blocked_by')
                if is_blocked(bug_id):
                    logger.info(
                        'Test skipped: - [%s]: %s' % (
                            item.nodeid.split(':')[0], values.get('description')))
                    test_instance = (item, 'SKIPPED', None)

                    test_result = create_result_object(test_instance, 0, 0)
                    self.completed_tests.append(test_result)
                    pytest.skip(item)

    def pytest_runtest_call(self, item):
        """ called to execute the test ``item``. """
        logger.info(
            'Executing: - [%s]: %s' % (
                item.nodeid.split(':')[0], item.own_markers[0].kwargs.get('description')))
        try:
            if item.funcargs['firefox']:
                item.funcargs['firefox'].start()
        except (AttributeError, KeyError):
            pass

    def pytest_runtest_teardown(self, item):
        BaseTarget.pytest_runtest_teardown(self, item)
        try:
            if item.funcargs['firefox'].runner and item.funcargs['firefox'].runner.process_handler:
                from targets.firefox.firefox_ui.helpers.keyboard_shortcuts import quit_firefox
                quit_firefox()
                status = item.funcargs['firefox'].runner.process_handler.wait(10)
                if status is None:
                    item.funcargs['firefox'].browser.runner.stop()
                if not target_args.save:
                    import shutil
                    profile_instance = item.funcargs['firefox'].profile
                    if os.path.exists(profile_instance.profile):
                        try:
                            shutil.rmtree(profile_instance.profile)
                        except OSError as e:
                            print("Error: %s - %s." % (e.filename, e.strerror))
                    else:
                        logger.error('Invalid Path!')
        except (AttributeError, KeyError):
            pass

    @pytest.fixture()
    def firefox(self, request):
        profile_type = request.node.own_markers[0].kwargs.get('profile')
        preferences = request.node.own_markers[0].kwargs.get('preferences')
        profile = FirefoxProfile.make_profile(profile_type, preferences)

        fx = target_args.firefox
        locale = core_args.locale
        app = FX_Collection.get(fx, locale)

        if not app:
            FX_Collection.add(fx, locale)
            app = FX_Collection.get(fx, locale)

        if target_args.update_channel:
            set_update_channel_pref(app.path, target_args.update_channel)
        Target.values = {'fx_version': app.version, 'fx_build_id': app.build_id, 'channel': app.channel}
        return FXRunner(app, profile)

        # BaseTarget.pytest_runtest_makereport(self, item, call)
        #
        # outcome = yield
        # report = outcome.get_result()
        #
        # if report.when == "call":
        #     test_case_instance = item.instance
        #     test_object_result = TestRailTests(test_case_instance.meta,
        #                                        test_case_instance.test_suite_id, test_case_instance.test_case_id,
        #                                        test_case_instance.blocked_by, test_case_instance.test_results)
        #
        #     self.test_run_object_list.append(test_object_result)
