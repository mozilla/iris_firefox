# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *



class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test of the 'About Firefox' window controls"


    def run(self):
        click_hamburger_menu_option("Help")
        click("about_firefox.png")
        if exists("x_button_about_firefox.png", 10):
            print "'About Firefox' window was opened successfully"
            click("x_button_about_firefox.png")
            if waitVanish("about_firefox_window_title.png", 10):
                print "'About Firefox' window was closed successfully"
                result = "PASS"
            else:
                print "'About Firefox' window is still open"
                result = "FAIL"
        else:
            print "'About Firefox' window is not open"
            result = "FAIL"

        print result