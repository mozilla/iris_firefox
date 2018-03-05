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
        url="about:config"
        preference="browser.newtabpage.activity-stream.enabled"

        navigate(url)
        change_preference(preference,"false")
        new_tab()
        new_tab()

        # Verify that activity stream has been disabled
        if exists("top_sites.png", 5):
            result = "FAIL"
        else:
            result = "PASS"

        print (result)

        navigate(url)
        change_preference(preference,"true")
        new_tab()
        new_tab()

        # Verify that activity stream has been enabled
        if exists("top_sites.png", 5):
            result = "PASS"
        else:
            result = "FAIL"

        print (result)
