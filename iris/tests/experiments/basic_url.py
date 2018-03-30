# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.



from test_case import *


class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        self.meta = "This is a test of basic URL navigation via awesomebar"


    def run(self):

        url = "https://www.google.com/?hl=EN"
        # helper function from "awesome_bar"
        navigate(url)

        # image: "Google Search" button
        # details: below the search field in page content
        # location: www.google.com
        image = "google_search.png"

        # core api function
        if exists(image, 10):
            result = "PASS"
        else:
            result = "FAIL"

        print result
