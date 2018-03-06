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
    sys.path.append(app.tests_package)
    # Start with no saved profiles
    clean_profiles()

    # Then we'd dynamically call test() and run on this list of test cases
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
