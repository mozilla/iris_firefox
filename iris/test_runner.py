# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import importlib

from api.core.profile import Profile
from api.core.util.json_utils import create_log_object, update_log_object, append_logs
from api.helpers.general import *
from email_report.email_client import EmailClient
from iris.test_rail.test_rail_client import *

logger = logging.getLogger(__name__)


def run(master_tests_list, test_list, browser):
    passed = failed = skipped = errors = 0
    logger.info('Running tests')
    start_time = time.time()

    test_failures = []
    tests_blocked = []
    test_case_results = []
    test_log = {}
    for index, module in enumerate(test_list, start=1):

        current_module = importlib.import_module(module)
        IrisCore.set_current_module(current_module.__file__)

        try:
            current = current_module.Test()
            current.browser = browser
            current.base_local_web_url = IrisCore.get_base_local_web_url()
            current.index = index
            current.total_tests = len(test_list)
        except AttributeError:
            test_failures.append(module)
            logger.warning('[%s] is not a test file. Skipping...', module)
            return
        logger.info('\n' + '-' * 120)

        if IrisCore.verify_test_compat(current, browser) or parse_args().override:
            logger.info('Executing: %s - [%s]: %s' % (index, module, current.meta))
            current.start_time = time.time()

            reset_mouse()
            current.setup()

            try:
                profile = Profile.make_profile(current.profile)
                current.profile_path = profile
                profile.set_preferences(current.prefs)
            except ValueError:
                logger.error('Error creating profile')

            args = create_firefox_args(current)
            current.firefox_runner = launch_firefox(path=browser.path,
                                                    profile=current.profile_path,
                                                    url=current.url,
                                                    args=args)
            current.firefox_runner.start()

            fx_args = ','.join(current.firefox_runner.command)

            try:
                confirm_firefox_launch()
                if current.maximize_window:
                    maximize_window()
                current.run()
                passed += 1
            except AssertionError:
                test_failures.append(module)
                failed += 1
            except FindError:
                test_failures.append(module)
                failed += 1
                current.add_results(Result('FAILED', None, None, None, print_error(traceback.format_exc())))
            except (APIHelperError, ValueError, ConfigError, TypeError):
                test_failures.append(module)
                errors += 1
                current.add_results(Result('ERROR', None, None, None, print_error(traceback.format_exc())))

            current.end_time = time.time()

            try:
                current.teardown()
            except (FindError, APIHelperError):
                logger.info('Could not find the necessary patterns during cleanup on test case : %s - %s' % (index, current.meta))

            close_firefox(current)
            print_results(module, current)
            test_case_results.append(current.create_collection_test_rail_result())
            test_log_object = create_log_object(current_module, current, fx_args)

            current_package = os.path.split(os.path.dirname(current_module.__file__))[1]
            if current_package not in test_log:
                test_log[current_package] = []
            test_log[current_package].append(update_log_object(test_log_object))
        else:
            skipped += 1
            if current.blocked_by.get('id') and len(current.blocked_by.get('id')) > 0:
                tests_blocked.append(module)
            logger.info('Skipping disabled test case: %s - %s' % (index, current.meta))

    end_time = time.time()
    test_results = print_report_footer(Settings.get_os(), browser.version,
                                       browser.build_id, passed, failed, skipped, errors,
                                       get_duration(start_time, end_time), failures=test_failures,
                                       blocked=tests_blocked)

    if parse_args().report:
        test_rail_report = TestRail()
        test_rail_report.create_test_plan(browser.build_id, browser.version, test_case_results)

    if parse_args().email:
        email_report = EmailClient()
        email_report.send_email_report(browser.version, test_results, IrisCore.get_git_details())

    write_test_failures(test_failures, master_tests_list)
    append_logs(browser, test_list, master_tests_list, passed, test_failures, skipped, errors, start_time, end_time,
                tests=test_log)
    return
