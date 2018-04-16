# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        BaseTest.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test of the 'About Firefox' window controls"

    def run(self):
        # Helper function in general.py
        open_about_firefox()
        if exists("firefox_in_about.png", 10):
            print "'About Firefox' window was opened successfully"
            close_auxiliary_window()
            if waitVanish("firefox_in_about.png", 10):
                print "'About Firefox' window was closed successfully"
                result = "PASS"
            else:
                print "'About Firefox' window is still open"
                result = "FAIL"
        else:
            print "'About Firefox' window was not opened"
            result = "FAIL"

        print result