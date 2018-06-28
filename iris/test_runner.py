# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import importlib
import sys
import traceback

from api.helpers.general import *
from api.helpers.results import *
from api.helpers.version_parser import check_version

logger = logging.getLogger(__name__)


def run(app):
    passed = failed = skipped = errors = 0
    logger.info('Running tests')
    start_time = time.time()
    # Start with no saved profiles
    clean_profiles()

    load_tests(app)
    for package in app.test_packages:
        sys.path.append(package)

    test_failures = []
    for index, module in enumerate(app.test_list, start=1):

        current_module = importlib.import_module(module)
        try:
            current = current_module.Test(app)
        except AttributeError:
            test_failures.append(module)
            logger.warning('[%s] is not a test file. Skipping...', module)
            return
        logger.info('\n' + '-' * 120)

        is_correct_version = True if current.fx_version == '' else check_version(app.version, current.fx_version)

        if (Settings.getOS() not in current.exclude and is_correct_version) or app.args.override:
            logger.info('Executing: %s - [%s]: %s' % (index, module, current.meta))
            current.set_start_time(time.time())

            # Move the mouse to upper left corner of the screen
            reset_mouse()

            # Set up test case conditions
            current.setup()

            # Process test case setup values and launch Firefox
            write_profile_prefs(current)
            args = create_firefox_args(current)
            launch_firefox(path=app.fx_path, profile=current.profile, url=current.url, args=args)

            # Verify that Firefox has launched
            confirm_firefox_launch(app)

            # Adjust Firefox window size
            if current.maximize_window:
                maximize_window()

            # Run the test logic
            try:
                current.run()
            except AssertionError:
                test_failures.append(module)
                failed += 1
                current.set_end_time(time.time())
                print_results(module, current)
                current.teardown()
                quit_firefox()
                confirm_firefox_quit(app)
                continue
            except FindError:
                test_failures.append(module)
                failed += 1
                current.add_results('FAILED', None, None, None, print_error(traceback.format_exc()))
                current.set_end_time(time.time())
                print_results(module, current)
                current.teardown()
                quit_firefox()
                confirm_firefox_quit(app)
                continue
            except (APIHelperError, ValueError, ConfigError, UnsupportedAttributeError, UnsupportedMethodError,
                    UnsupportedClassMethodError, TypeError):
                test_failures.append(module)
                errors += 1
                current.add_results('ERROR', None, None, None, print_error(traceback.format_exc()))
                current.set_end_time(time.time())
                print_results(module, current)
                current.teardown()
                quit_firefox()
                confirm_firefox_quit(app)
                continue

            passed += 1
            current.set_end_time(time.time())
            # Quit Firefox
            print_results(module, current)
            current.teardown()
            quit_firefox()
            confirm_firefox_quit(app)
        else:
            skipped += 1
            logger.info('Skipping disabled test case: %s - %s' % (index, current.meta))

    end_time = time.time()
    print_report_footer(Settings.getOS(), app.version, app.build_id, passed, failed, skipped, errors,
                        get_duration(start_time, end_time), failures=test_failures)

    # We may remove profiles here, but likely still in use and can't do it yet
    # clean_profiles()
    app.finish()

def write_profile_prefs(test_case):
    if len(test_case.prefs):
        pref_file = os.path.join(test_case.profile, 'user.js')
        file = open(pref_file, 'w')
        for pref in test_case.prefs:
            name, value = pref.split(';')
            file.write('user_pref("%s", %s);\n' % (name, value))
        file.close()

def create_firefox_args(test_case):
    args = []
    if test_case.private_browsing:
        args.append('-private')

    if test_case.private_window:
        args.append('-private-window')

    try:
        if test_case.window_size:
            w, h = test_case.window_size.split('x')
            args.append('-width')
            args.append('%s' % w)
            args.append('-height')
            args.append('%s' % h)
            test_case.maximize_window = False
            if int(w) < 600:
                logger.warning('Windows of less than 600 pixels wide may cause Iris to fail.')
    except ValueError:
            logger.error('Incorrect window size specified. Must specify width and height separated by lowercase x.')

    if test_case.profile_manager:
        args.append('-ProfileManager')

    if test_case.set_default_browser:
        args.append('-setDefaultBrowser')

    if test_case.import_wizard:
        args.append('-migration')

    if test_case.search:
        args.append('-search')
        args.append(test_case.search)

    if test_case.preferences:
        args.append('-preferences')

    if test_case.devtools:
        args.append('-devtools')

    if test_case.js_debugger:
        args.append('-jsdebugger')

    if test_case.js_console:
        args.append('-jsconsole')

    if test_case.safe_mode:
        args.append('-safe-mode')

    return args


def load_tests(app):
    """Test loading

    Test loading is done by providing a test name, a path to a file containing a custom list of tests or a directory.
    The provided test name can be with or without .py extension
    The path to the file that contains the list of tests should have .txt extension. The full path is needed. For
    example: '/Users/user_name/full_path/test_suite.txt'. The content of the file should be a simple line-delimited list
    of test paths (full path required including file extensions).
    """
    app.test_list = []
    app.test_packages = []

    if app.args.test:
        if app.args.test.endswith('.txt'):
            suite_path = app.args.test
            if os.path.isfile(suite_path):
                logger.debug('"%s" found. Proceeding ...' % suite_path)
                with open(suite_path, 'r') as f:
                    test_paths_list = [line.strip() for line in f]
                if len(test_paths_list) == 0:
                    logger.error('"%s" does not contain any valid test paths. Exiting program ...' % str(suite_path))
                    app.finish(code=1)
                logger.debug('Tests found in the test suite file:\n\n%s\n' % '\n'.join(map(str, test_paths_list)))
                logger.debug('Validating test paths ...')
                for test_path in test_paths_list:
                    if os.path.isfile(test_path):
                        logger.debug('"%s" is a valid test path. Proceeding ...' % test_path)
                        app.test_list.append(os.path.splitext(os.path.basename(test_path))[0])
                        app.test_packages.append(os.path.dirname(test_path))
                    else:
                        logger.warning('"%s" is not a valid test path. Skipping ...' % test_path)

                if len(app.test_list) == 0:
                    logger.error('"%s" does not contain any valid test paths. Exiting program ...' % str(suite_path))
                    app.finish(code=1)
            else:
                logger.error('Could not locate "%s" . Exiting program ...', str(suite_path))
                app.finish(code=1)
            logger.debug('List of tests to execute: [%s]' % ', '.join(map(str, app.test_list)))
            return

        test_name = str(app.args.test + ('.py' if not app.args.test.endswith('.py') else '')).strip()
        tests_directory = os.path.join(os.path.split(__file__)[0], 'tests')
        for dir_path, sub_dirs, all_files in os.walk(tests_directory):
            if test_name in all_files:
                app.test_list.append(os.path.splitext(test_name)[0])
                app.test_packages.append(os.path.join(os.path.split(__file__)[0], dir_path.strip()))
        if len(app.test_list) == 0:
            logger.error('Could not locate %s . Exiting program ...' % str(test_name))
            app.finish(code=1)
        else:
            logger.debug('%s found. Proceeding ...' % test_name)
        return

    # There is always a default test directory,
    # but this can be overridden via command line
    tests_directory = os.path.join(os.path.split(__file__)[0], app.args.directory.strip())

    if os.path.isdir(tests_directory):
        logger.debug('Path %s found. Checking content ...', tests_directory)
        for dir_path, sub_dirs, all_files in os.walk(tests_directory):
            for current_file in all_files:
                if current_file.endswith('.py') and not current_file.startswith('__'):
                    app.test_list.append(os.path.splitext(current_file)[0])
                    if dir_path not in app.test_packages:
                        app.test_packages.append(dir_path)
        if len(app.test_list) == 0:
            logger.error('Directory %s does not contain test files. Exiting program ...' % tests_directory)
            app.finish(code=1)
        else:
            logger.debug('Test packages: %s', app.test_packages)
            logger.debug('List of tests to execute: [%s]' % ', '.join(map(str, app.test_list)))
    else:
        logger.error('Path: %s does not exist. Exiting program ...' % tests_directory)
        app.finish(code=1)
