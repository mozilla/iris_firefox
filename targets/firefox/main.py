# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import logging
import os
import sqlite3
from multiprocessing import Process
import shutil

import pytest

from src.base.target import BaseTarget
from src.core.api.mouse.mouse import mouse_reset
from src.core.api.os_helpers import OSHelper
from src.core.util.arg_parser import get_core_args
from src.core.util.local_web_server import LocalWebServer
from src.core.util.path_manager import PathManager
from src.core.util.test_assert import create_result_object

logger = logging.getLogger(__name__)
logger.info('Loading test images...')

from src.configuration.config_parser import validate_section
from targets.firefox.bug_manager import is_blocked
from targets.firefox.firefox_app.fx_browser import FXRunner, FirefoxProfile, FirefoxUtils
from targets.firefox.firefox_app.fx_collection import FX_Collection
from targets.firefox.firefox_ui.helpers.keyboard_shortcuts import quit_firefox
from targets.firefox.firefox_ui.helpers.version_parser import check_version
from targets.firefox.testrail.testrail_client import report_test_results

target_args = None
core_args = get_core_args()


class Target(BaseTarget):
    test_run_object_list = []
    index = 1

    def __init__(self):
        BaseTarget.__init__(self)
        global target_args
        target_args = self.get_target_args()
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

    def get_target_args(self):
        parser = argparse.ArgumentParser(description='Firefox-specific arguments', prog='iris')
        parser.add_argument('-f', '--firefox',
                            help='Firefox version to test',
                            action='store',
                            default='latest-beta')
        parser.add_argument('-r', '--report',
                            help='Report tests to TestRail',
                            action='store_true')
        parser.add_argument('-u', '--update_channel',
                            help='Update channel profile preference',
                            action='store')
        parser.add_argument('-s', '--save',
                            help='Save Firefox profiles on disk',
                            action='store_true')

        return parser.parse_known_args()[0]

    def validate_config(self):
        if self.args.report:
            rep_s = validate_section('Test_rail')
            if len(rep_s) > 0:
                logger.warning('{}. Report tests to TestRail was disabled.'.format(rep_s))
                self.args.report = False

        bugzilla_s = validate_section('Bugzilla')
        if len(bugzilla_s) > 0:
            logger.warning('{}. Tests blocked by Bugzilla issues will be automatically skipped.'.format(bugzilla_s))

        git_hub_s = validate_section('GitHub')
        if len(bugzilla_s) > 0:
            logger.warning('{}. Tests blocked by GitHub issues will be automatically skipped.'.format(git_hub_s))

    def pytest_sessionstart(self, session):
        global core_args
        core_args = get_core_args()
        global target_args
        BaseTarget.pytest_sessionstart(self, session)
        self.validate_config()
        try:
            port = core_args.port

            logger.info('Starting local web server on port %s for directory %s' % (port, self.local_web_root))
            web_server_process = Process(target=LocalWebServer, args=(self.local_web_root, port,))
            self.process_list.append(web_server_process)
            web_server_process.start()

            fx = self.args.firefox
            locale = core_args.locale
            app = FX_Collection.get(fx, locale)

            if not app:
                FX_Collection.add(fx, locale)
                app = FX_Collection.get(fx, locale)
            self.values = {'fx_version': app.version, 'fx_build_id': app.build_id, 'channel': app.channel}
        except IOError:
            logger.critical('Unable to launch local web server, aborting Iris.')
            exit(1)
        logger.info('Loading more test images...')

    def pytest_sessionfinish(self, session):
        BaseTarget.pytest_sessionfinish(self, session)
        for process in self.process_list:
            logger.info('Terminating process.')
            process.terminate()
            process.join()
        logger.debug('Finishing Firefox session')
        if target_args.report:
            report_test_results(self)

    def pytest_runtest_setup(self, item):
        BaseTarget.pytest_runtest_setup(self, item)

        if OSHelper.is_mac():
            mouse_reset()
        if item.name == 'run':
            skip_reason_list = []
            values = item.own_markers[0].kwargs
            is_disabled = 'enabled' in values and not values.get('enabled') and not core_args.override
            is_excluded = 'exclude' in values and OSHelper.get_os() in values.get('exclude')
            incorrect_locale = 'locale' in values and core_args.locale not in values.get('locale')
            incorrect_platform = 'platform' in values and OSHelper.get_os() not in values.get('platform')
            fx_version = self.values.get('fx_version')
            incorrect_fx_version = 'fx_version' in values and not check_version(fx_version, values.get('fx_version'))

            if is_disabled:
                skip_reason_list.append('Test is disabled')

            if is_excluded:
                skip_reason_list.append('Test is excluded for {}'.format(OSHelper.get_os()))

            if 'blocked_by' in values:
                bug_id = values.get('blocked_by')
                if is_blocked(bug_id):
                    skip_reason_list.append('Test is blocked by [{}]'.format(bug_id))

            if incorrect_locale:
                skip_reason_list.append('Test doesn\'t support locale [{}]'.format(core_args.locale))

            if incorrect_platform:
                skip_reason_list.append('Test doesn\'t support platform [{}]'.format(OSHelper.get_os()))

            if incorrect_fx_version:
                skip_reason_list.append('Test doesn\'t support Firefox version [{}]'.format(fx_version))

            if len(skip_reason_list) > 0:
                logger.info(
                    'Test skipped: - [{}]: {} Reason(s): {}'.format(item.nodeid.split(':')[0],
                                                                    values.get('description'),
                                                                    ', '.join(skip_reason_list)))
                test_instance = (item, 'SKIPPED', None)

                test_result = create_result_object(test_instance, 0, 0)
                self.completed_tests.append(test_result)
                pytest.skip(item)

    def pytest_runtest_call(self, item):
        """ called to execute the test ``item``. """

        logger.info(
            'Executing %s: - [%s]: %s' % (self.index,
                item.nodeid.split(':')[0], item.own_markers[0].kwargs.get('description')))
        self.index += 1
        try:
            if item.funcargs['firefox']:
                item.funcargs['firefox'].start()
        except (AttributeError, KeyError):
            pass

    def pytest_runtest_teardown(self, item):
        BaseTarget.pytest_runtest_teardown(self, item)

        try:
            if not OSHelper.is_windows():
                if item.funcargs['firefox'].runner and item.funcargs['firefox'].runner.process_handler:
                    quit_firefox()
                    status = item.funcargs['firefox'].runner.process_handler.wait(10)
                    if status is None:
                        item.funcargs['firefox'].browser.runner.stop()
            else:
                item.funcargs['firefox'].stop()
            if not target_args.save:
                profile_instance = item.funcargs['firefox'].profile
                if os.path.exists(profile_instance.profile):
                    try:
                        shutil.rmtree(profile_instance.profile, ignore_errors=True)
                    except sqlite3.OperationalError:
                        pass
                else:
                    logger.error('Invalid Path: %s' % profile_instance.profile)
        except (AttributeError, KeyError):
            pass

    @pytest.fixture()
    def firefox(self, request):
        profile_type = request.node.own_markers[0].kwargs.get('profile')
        preferences = request.node.own_markers[0].kwargs.get('profile_preferences')
        profile = FirefoxProfile.make_profile(profile_type, preferences)

        fx = target_args.firefox
        locale = get_core_args().locale
        app = FX_Collection.get(fx, locale)

        if not app:
            FX_Collection.add(fx, locale)
            app = FX_Collection.get(fx, locale)

        if target_args.update_channel:
            FirefoxUtils.set_update_channel_pref(app.path, target_args.update_channel)
        return  FXRunner(app, profile)

