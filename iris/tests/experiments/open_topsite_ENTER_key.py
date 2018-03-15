# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *



class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test for opening the first default topsite from TOP SITES list by pressing the ENTER key"


    def run(self):
        url = "about:home"
        navigate(url)

        number_of_iterations = 1
        if exists("top_sites.png", 10):
            #  The TOP SITES section is populated by default with the sites listed in the following document https://docs.google.com/spreadsheets/d/15yLsFBkic5DFUSdbvSFlR3Rzjxqwmizq9EmksK28l6I/edit#gid=170333837
            #  Focus the first default TOP SITE and press the ENTER key
            while number_of_iterations <= 8:
                focus_next_item()
                number_of_iterations += 1
            type(Key.ENTER)

            # Check that the first default TOP SITE is opened
            if exists("youtube.png", 10):
                print "PASS"
            else:
                print "FAIL"
        else:
            print "FAIL"

