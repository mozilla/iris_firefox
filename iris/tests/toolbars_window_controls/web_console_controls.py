# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *


class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test case that checks if the Web Console controls work as expected"

    def run(self):

        url = "about:home"
        navigate(url)

        open_web_console()

        time.sleep(5)

        buttons = ["dock_to_side.png", "separate_window.png", "close_dev_tools.png"]

        a = 0
        found = False
        for i in buttons:
            if exists(i, 3):
                a = a + 1
            if a == len(buttons):
                logger.debug("Found all buttons")
                found = True

        if found:
            hover("close_dev_tools.png")
            time.sleep(2)




        click("close_dev_tools.png")

        time.sleep(2)