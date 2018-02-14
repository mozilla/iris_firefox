# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *



class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test of a bunch of tabs"


    def run(self):

        fx_ui = "refresh.png"

        # core api function
        wait(fx_ui, 10)

        # helper function
        new_tab()
        new_tab()
        new_tab()
        new_tab()
        new_tab()
        new_tab()
        new_tab()
        new_tab()
        new_tab()
        new_tab()

        # core api function
        if exists(fx_ui, 5):
            result = "PASS"
        else:
            result = "FAIL"

        print (result)
