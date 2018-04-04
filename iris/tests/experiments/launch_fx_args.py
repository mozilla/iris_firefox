# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *

import time


class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        self.meta = "This is a test of creating various Firefox instances with arguments"

    def run(self):
        amazon_image = "amazon.png"

        amazon_image = "amazon.png"

        time.sleep(5)
        args = ["-width", "800", "-height", "800", "-new-tab", "http://www.mozilla.org"]
        launch_firefox(path=self.app.fx_path, profile="size_800", args=args)

        time.sleep(5)
        args = ["-width", "600", "-height", "600", "-search", "firefox"]
        launch_firefox(path=self.app.fx_path, profile="size_600", args=args)

        time.sleep(5)
        args = ["-width", "400", "-height", "400", "-private-window", "http://amazon.com"]
        launch_firefox(path=self.app.fx_path, profile="size_400", args=args)

        expected_1 = exists(amazon_image, 1)
        assert_true(self, expected_1, 'Find amazon image')

        quit_firefox()
        time.sleep(5)
        quit_firefox()
        time.sleep(5)
        quit_firefox()
        time.sleep(5)
