# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *



class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test of the 'About Firefox' window"


    def run(self):
        new_tab()
        close_window()
        if exists("close_multiple_tabs_warning.png", 10):
            print "Close multiple tabs warning was displayed successfully"
            close_auxiliary_window()
            if (waitVanish("close_multiple_tabs_warning.png", 10) and exists("home_button.png", 10)):
                print "Close multiple tabs warning was canceled successfully"
            else:
                print "Close multiple tabs warning was not canceled successfully"
                result = "FAIL"
        else:
            print "Close multiple tabs warning was not displayed"
            result = "FAIL"
        close_window()
        if exists("close_multiple_tabs_warning.png", 10):
            print "Close multiple tabs warning was displayed successfully"
            click("close_multiple_tabs_warning.png")
            if (waitVanish("close_multiple_tabs_warning.png", 10) and waitVanish("home_button.png", 10)):
                print "The browser was closed successfully"
                result = "PASS"
            else:
                print "The browser was not closed successfully"
                result = "FAIL"

        print result
