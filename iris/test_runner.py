# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from api.helpers.general import *
from logger.iris_logger import *
import os
import sys
import importlib


logger = getLogger(__name__)

def run(app):
    logger.info("Running tests")

    # Start with no saved profiles
    clean_profiles()

    load_tests(app)
    sys.path.append(app.tests_package)

    for module in app.tests_list:
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
    app.tests_list = []
    app.tests_package = None

    if app.args.directory:
        tests_directory = os.path.join(os.path.split(__file__)[0], app.args.directory.strip())
        if (os.path.isdir(tests_directory)):
            logger.info("Path %s found. Checking content ...", tests_directory)
            for file in os.listdir(tests_directory):
                if file.endswith(".py") and not file.startswith("__init__"):
                    app.tests_list.append(os.path.splitext(file)[0])
            if len(app.tests_list) == 0:
                logger.error("Directory %s does not contain test files. Exiting program ...", tests_directory)
                exit(1)
            else:
                app.tests_package = tests_directory
                logger.info("Test package: %s", app.tests_package)
                logger.info("List of tests to execute: [%s]" % ', '.join(map(str, app.tests_list)))
        else:
            logger.error("Path: %s does not exist. Exiting program ...", tests_directory)
            exit(1)
    elif app.args.test:
        test_name = str(app.args.test + ('.py' if not app.args.test.endswith('.py') else '')).strip()
        tests_directory = os.path.join(os.path.split(__file__)[0], "tests")
        for dirpath, subdirs, files in os.walk(tests_directory):
            if test_name in files:
                app.tests_list.append(os.path.splitext(test_name)[0])
                app.tests_package = os.path.join(os.path.split(__file__)[0], dirpath.strip())
        if len(app.tests_list) == 0:
            logger.error("Could not locate %s . Exiting program ...", str(test_name))
            exit(1)
        else:
            logger.info("FOUND %s", test_name)
    else:
        # what is default behavior w/o these two arguments?
        pass
