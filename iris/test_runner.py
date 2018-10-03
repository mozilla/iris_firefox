# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import importlib

from api.core.profile import *
from api.helpers.general import *
from email_report.email_client import EmailClient
from iris.test_rail.test_rail_client import *

logger = logging.getLogger(__name__)


def run(app):
    passed = failed = skipped = errors = 0
    logger.info('Running tests')
    start_time = time.time()

    test_failures = []
    test_case_results = []
    test_log = {}

    for index, module in enumerate(app.test_list, start=1):

        current_module = importlib.import_module(module)
        set_current_module(current_module.__file__)

        try:
            current = current_module.Test(app)
            app.current_test += 1
        except AttributeError:
            test_failures.append(module)
            logger.warning('[%s] is not a test file. Skipping...', module)
            return
        logger.info('\n' + '-' * 120)

        if verify_test_compat(current, app) or app.args.override:
            logger.info('Executing: %s - [%s]: %s' % (index, module, current.meta))
            current.set_start_time(time.time())

            # Move the mouse to upper left corner of the screen
            reset_mouse()

            # Set up test case conditions
            current.setup()

            # Generate profile
            try:
                current.profile_path = Profile.make_profile(current.profile)
            except ValueError:
                app.finish(code=1)

            # Process test case setup values and launch Firefox
            write_profile_prefs(current)
            args = create_firefox_args(current)
            fx_args = launch_firefox(path=app.fx_path, profile=current.profile_path, url=current.url, args=args)

            # Verify that Firefox has launched
            confirm_firefox_launch(app)

            # Adjust Firefox window size
            if current.maximize_window:
                maximize_window()

            # Run the test logic.
            try:
                current.run()
                passed += 1
            except AssertionError:
                test_failures.append(module)
                failed += 1
            except FindError:
                test_failures.append(module)
                failed += 1
                current.add_results('FAILED', None, None, None, print_error(traceback.format_exc()))
            except (APIHelperError, ValueError, ConfigError, TypeError):
                test_failures.append(module)
                errors += 1
                current.add_results('ERROR', None, None, None, print_error(traceback.format_exc()))

            current.set_end_time(time.time())
            print_results(module, current)
            test_case_results.append(current.create_collection_test_rail_result())

            # Initialize test log object
            test_log_object = create_log_object(current_module, current, fx_args)

            # Clean up and quit Firefox.
            current.teardown()
            quit_firefox()
            if current.profile == Profile.BRAND_NEW:
                confirm_close_multiple_tabs()
            confirm_firefox_quit(app)

            # Save current test log
            current_package = os.path.split(os.path.dirname(current_module.__file__))[1]
            if not current_package in test_log:
                test_log[current_package] = []
            test_log[current_package].append(update_log_object(test_log_object))

        else:
            skipped += 1
            logger.info('Skipping disabled test case: %s - %s' % (index, current.meta))

    end_time = time.time()
    test_results = print_report_footer(Settings.get_os(), app.version, app.build_id, passed, failed, skipped, errors,
                                       get_duration(start_time, end_time), failures=test_failures)

    if app.args.report:
        test_rail_report = TestRail()
        test_rail_report.create_test_plan(app.build_id, app.version, test_case_results)

    if app.args.email:
        email_report = EmailClient()
        email_report.send_email_report(app.version, test_results, get_git_details())

    app.write_test_failures(test_failures)
    append_logs(app, passed, failed, skipped, errors, start_time, end_time, tests=test_log)
    app.finish()


def create_log_object(module, current, fx_args):
    run_obj = {'name': module.__name__, 'meta': current.meta, 'profile': current.profile,
               'module': module.__file__, 'profile_path': current.profile_path,
               'fx_args': fx_args, 'prefs': current.prefs,
               'time': int(current.get_end_time() - current.get_start_time())}
    run_obj['asserts'] = []
    outcome = 'PASSED'
    for result in current.results:
        if result.outcome is 'FAILED':
            outcome = result.outcome
        run_obj['asserts'].append({'outcome': result.outcome, 'message': result.message,
                                   'expected': result.expected, 'actual': result.actual,
                                   'error': result.error})
        run_obj['result'] = outcome
    return run_obj


def update_log_object(run_obj):
    # If debug images were created for this test, add their names to the log file.
    if os.path.exists(get_image_debug_path()):
        debug_images = []
        for root, dirs, files in os.walk(get_image_debug_path()):
            for file_name in files:
                debug_images.append(file_name)
        run_obj['debug_images'] = sorted(debug_images)
        run_obj['debug_image_directory'] = get_image_debug_path()
    return run_obj


def append_logs(app, passed, failed, skipped, errors, start_time, end_time, tests):
    # First, update the runs.json log.
    app.update_run_index({'total': len(app.test_list), 'failed': failed})

    # Second, update the run.json log for this particular run.
    data = {'total': len(app.test_list), 'passed': passed, 'failed': failed,
            'skipped': skipped, 'errors': errors, 'start_time': int(start_time),
            'end_time': int(end_time), 'total_time': int(get_duration(start_time, end_time)),
            'tests': tests}
    app.update_run_log(data)
