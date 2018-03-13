# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from api.helpers.general import *
from logger.iris_logger import *
import os
import sys
import importlib

def run(app):
    print app.args
    logger = initialize_logger(app)
    logger.info("Running tests")

    # Start with no saved profiles
    clean_profiles()

    load_tests(app)
    for package in app.test_packages:
        sys.path.append(package)

    for module in app.test_list:
        current_module = importlib.import_module(module)
        current = current_module.test(app)
        logger.info("Running test case: %s " % current.meta)

        # Initialize and launch Firefox
        current.setup()

        # Verify that Firefox has launched
        confirm_firefox_launch()

        # Run the test logic
        current.run()

        # Quit Firefox
        current.teardown()
        confirm_firefox_quit()


    # We may remove profiles here, but likely still in use and can't do it yet
    #clean_profiles()


def load_tests(app):
    logger = initialize_logger(app)
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
            logger.info("FOUND %s", test_name)
        return

    # There is always a default test directory,
    # but this can be overridden via command line
    tests_directory = os.path.join(os.path.split(__file__)[0], app.args.directory.strip())

    if (os.path.isdir(tests_directory)):
        logger.debug("Path %s found. Checking content ...", tests_directory)
        for dirpath, subdirs, files in os.walk(tests_directory):
            for file in files:
                if file.endswith(".py") and not file.startswith("__init__"):
                    app.test_list.append(os.path.splitext(file)[0])
                    if not dirpath in app.test_packages:
                        app.test_packages.append(dirpath)
        if len(app.test_list) == 0:
            logger.error("Directory %s does not contain test files. Exiting program ...", tests_directory)
            exit(1)
        else:
            logger.info("Test packages: %s", app.test_packages)
            logger.info("List of tests to execute: [%s]" % ', '.join(map(str, app.test_list)))
    else:
        logger.error("Path: %s does not exist. Exiting program ...", tests_directory)
        exit(1)

def initialize_logger(app):
    logger = getLogger(__name__)
    logger.setLevel(app.args.level)
    return logger
