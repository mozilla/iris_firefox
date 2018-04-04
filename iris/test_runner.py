# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from api.helpers.general import *
from api.helpers.results import *
import os
import sys
import importlib
import logging

logger = logging.getLogger(__name__)

passed = 0
failed = 0
skipped = 0


def run(app):
    logger.info("Running tests")
    start_time = time.time()
    # Start with no saved profiles
    clean_profiles()

    load_tests(app)
    for package in app.test_packages:
        sys.path.append(package)

    for module in app.test_list:

        current_module = importlib.import_module(module)
        try:
            current = current_module.test(app)
        except AttributeError:
            logger.warning('[%s] is not a test file. Skipping...', module)
            return
        logger.info('\n' + '-' * 120)
        if current.enable:
            logger.info("Executing: %s " % current.meta)
            current.set_start_time(time.time())

            # Move the mouse to upper left corner of the screen
            reset_mouse()

            # Initialize and launch Firefox
            current.setup()

            # Verify that Firefox has launched
            confirm_firefox_launch()

            # Adjust Firefox window size
            current.resize_window()

            # Run the test logic
            try:
                current.run()
            except AssertionError:
                global failed
                failed += 1
                current.set_end_time(time.time())
                current.teardown()
                confirm_firefox_quit()
                continue

            global passed
            passed += 1
            current.set_end_time(time.time())
            # Quit Firefox
            current.teardown()
            confirm_firefox_quit()
        else:
            global skipped
            skipped += 1
            logger.info("Skipping disabled test case: %s" % current.meta)

    end_time = time.time()
    print_report_footer(passed, failed, skipped, get_duration(start_time, end_time))

    # We may remove profiles here, but likely still in use and can't do it yet
    # clean_profiles()


def load_tests(app):

    app.test_list = []
    app.test_packages = []

    # Test loading is either by test or by directory
    # If a test name is provided, this will be used above all else
    if app.args.test:
        test_name = str(app.args.test + ('.py' if not app.args.test.endswith('.py') else '')).strip()
        tests_directory = os.path.join(os.path.split(__file__)[0], "tests")
        for dirpath, subdirs, files in os.walk(tests_directory):
            if test_name in files:
                app.test_list.append(os.path.splitext(test_name)[0])
                app.test_packages.append(os.path.join(os.path.split(__file__)[0], dirpath.strip()))
        if len(app.test_list) == 0:
            logger.error("Could not locate %s . Exiting program ...", str(test_name))
            exit(1)
        else:
            logger.debug("FOUND %s", test_name)
        return

    # There is always a default test directory,
    # but this can be overridden via command line
    tests_directory = os.path.join(os.path.split(__file__)[0], app.args.directory.strip())

    if (os.path.isdir(tests_directory)):
        logger.debug("Path %s found. Checking content ...", tests_directory)
        for dirpath, subdirs, files in os.walk(tests_directory):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    app.test_list.append(os.path.splitext(file)[0])
                    if not dirpath in app.test_packages:
                        app.test_packages.append(dirpath)
        if len(app.test_list) == 0:
            logger.error("Directory %s does not contain test files. Exiting program ...", tests_directory)
            exit(1)
        else:
            logger.debug("Test packages: %s", app.test_packages)
            logger.debug("List of tests to execute: [%s]" % ', '.join(map(str, app.test_list)))
    else:
        logger.error("Path: %s does not exist. Exiting program ...", tests_directory)
        exit(1)
