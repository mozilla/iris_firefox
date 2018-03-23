# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *


class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        self.meta = "This is a test for opening the first default topsite from TOP SITES list by clicking on it"

    def run(self):
        url = "about:home"
        navigate(url)

        if exists("top_sites.png", 10):
            click("youtube_top_site.png")
            # Check that the first default TOP SITE is opened
            if exists("youtube.png", 10):
                print ("PASS")
            else:
                print ("FAIL")
        else:
            print ("FAIL")
