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

        time.sleep(5)
        args = []
        args.append("-width")
        args.append("800")
        args.append("-height")
        args.append("800")
        args.append("-new-tab")
        args.append("http://www.mozilla.org")
        launch_firefox(path=self.app.fx_path, profile="size_800", args=args)

        time.sleep(5)
        args = []
        args.append("-width")
        args.append("600")
        args.append("-height")
        args.append("600")
        args.append("-search")
        args.append("firefox")
        launch_firefox(path=self.app.fx_path, profile="size_600", args=args)

        time.sleep(5)
        args = []
        args.append("-width")
        args.append("400")
        args.append("-height")
        args.append("400")
        args.append("-private-window")
        args.append("amazon.com")
        launch_firefox(path=self.app.fx_path, profile="size_400", args=args)

        if exists("amazon.png", 20):
            result = "PASS"
        else:
            result = "FAIL"
        print (result)

        quit_firefox()
        time.sleep(5)
        quit_firefox()
        time.sleep(5)
        quit_firefox()
        time.sleep(5)
