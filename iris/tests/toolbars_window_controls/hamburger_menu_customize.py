# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test case that checks the hamburger menu > Customize opens the customize page"

    def run(self):
        url = "about:home"
        navigate(url)

        # Open Customize from te Hamburger Menu
        click_hamburger_menu_option("Customize")

        # Check that the customize page is opened by searcing for text "overflow menu"
        try:
            wait("overflow menu", 10)
            print "PASS"
            logger.debug("customize page present")
        except:
            print "FAIL"
            logger.error("Can't find overflow menu text, aborting test.")
            return
        else:
            close_customize_page()
