# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *



class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This tests the ability to activate/deactivate the activity stream"


    def run(self):

        preference="browser.newtabpage.activity-stream.enabled"
        change_preference(preference, "false")
        new_tab()
        new_tab()
        time.sleep(2)

        # Verify that activity stream has been disabled
        if "TOP SITES" in get_firefox_region().text():
            result = "FAIL"
        else:
            result = "PASS"

        print (result)

        change_preference(preference, "true")
        new_tab()
        new_tab()
        time.sleep(2)

        # Verify that activity stream has been enabled
        if "TOP SITES" in get_firefox_region().text():
            result = "PASS"
        else:
            result = "FAIL"

        print (result)
