# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *


class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test case that checks if the Title Bar can be activated/deactivated properly from Customize menu"


    def run(self):
        url = "about:home"
        navigate(url)


        click_hamburger_menu_option("Customize")

        if exists("title_bar.png", 10):
            logger.info("Title Bar can be activated")
            click("title_bar.png")
            time.sleep(2)
            if exists("active_title_bar.png", 10):
                logger.debug("Title Bar has been activated")
                result = "PASS"
            else:
                logger.error("Title Bar can not be activated")
                result = "TRUE"
            print result

            #check if the Title Bar can be deactivated

            click("title_bar.png")
            if waitVanish("active_title_bar.png", 10):
                logger.debug("Title Bar has been successfully deactivated")
                result = "PASS"
            else:
                logger.error("Title Bar can NOT be deactivated")
                result = "FAIL"
        else:
            logger.error("Title Bar checkbox not found")
            result = "FAIL"
        print result






