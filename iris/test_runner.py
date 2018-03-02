# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from api.helpers.general import *

# Temporarily hard-coded for just a few tests
from tests.experiments import empty, tabs, back_forward, basic_url


# The test runner will be written so that it can iterate through the "tests"
# directory and dynamically import what it finds.
#
# Additionally, we will create logic to only run certain tests and test sets.


def run(app):
    print "test_runner.py: Running tests"


    # start with no saved profiles
    clean_profiles()

    # Hard-code for now, but we will build a dynamic array of tests to run later
    all_tests = []
    all_tests.append(tabs)
    all_tests.append(back_forward)
    all_tests.append(basic_url)

    # then we'd dynamically call test() and run on this list of test cases
    for module in all_tests:

        current = module.test(app)
        print "Running test case: %s " % current.meta

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
