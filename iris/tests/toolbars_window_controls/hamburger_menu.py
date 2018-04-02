# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *


class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test case that checks the 'click_hamburger_menu_option' function"

    def run(self):
        url = "about:home"
        navigate(url)

        #  Check that the 'click_hamburger_menu_option' function works as expected.
        click_hamburger_menu_option("customize")
        time.sleep(2)

        return
