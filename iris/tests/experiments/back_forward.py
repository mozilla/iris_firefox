# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from api.helpers.awesome_bar import *
from api.helpers.general import *
from api.helpers.keyboard_shortcuts import *
from test_case import *


class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test of browser back/forward"


    def run(self):
        #check to ensure firefox is running
        firefox_exists()

        url = "about:home"
        # helper function from "keyboard_shortcuts"
        navigate_to(url)

        if exists("search_the_web.png", 10):
            url = "www.google.com"

            # helper function from "keyboard_shortcuts"
            navigate_to(url)

            # core api function
            if exists("google_search.png", 10):

                # helper function from "awesome_bar"
                #back_in_history()
                navigate_back()

                # core api function
                if exists("search_the_web.png", 10):

                    # helper function from "awesome_bar"
                    #forward_in_history()
                    navigate_forward()

                    # core api function
                    if exists("google_search.png", 10):
                        result =  "PASS"
                    else:
                        result = "FAIL"
                else:
                    result = "FAIL"
            else:
                result = "FAIL"
        else:
            result = "FAIL"

        print result