# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import logging

from src.base.target import *
from targets.firefox.parse_args import parse_args
# from targets.firefox.testrail.testcase_results import TestRailTests

logger = logging.getLogger(__name__)


class Target(BaseTarget):

    test_run_object_list = []

    def __init__(self):
        BaseTarget.__init__(self)
        self.target_name = 'Firefox'

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

    @pytest.fixture(scope="class", autouse=True)
    def use_firefox(self, request):
        fx = args.firefox
        locale = args.locale

        browser = FX_Collection.get(fx, locale)
        if not browser:
            FX_Collection.add(fx, locale)
            browser = FX_Collection.get(fx, locale)
        browser.start()

        def teardown():
            if browser.runner:
                browser.runner.stop()

        request.addfinalizer(teardown)

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

