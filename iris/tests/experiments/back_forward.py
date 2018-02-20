# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *


class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test of browser back/forward"


    def run(self):

        url = "about:home"
        # helper function from "keyboard_shortcuts"
        navigate(url)

        if exists("search_the_web.png", 10):
            url = "www.google.com"

            # helper function from "keyboard_shortcuts"
            navigate(url)

            # core api function
            if exists("google_search.png", 10):

                try:
                    wait("back.png", 10)
                    click("back.png")

                    # core api function
                    if exists("search_the_web.png", 10):

                        try:
                            wait("forward.png", 10)
                            click("forward.png")

                            # core api function
                            if exists("google_search.png", 10):
                                result = "PASS"
                            else:
                                result = "FAIL"
                        except:
                            result = "FAIL"
                    else:
                        result = "FAIL"

                except:
                    result = "FAIL"
            else:
                result = "FAIL"
        else:
            result = "FAIL"

        print result
