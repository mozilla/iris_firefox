# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *



class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test of the 'Undo Close Tab' option in the tabs bar"


    def run(self):
        url = "https://www.google.com/?hl=EN"
        new_tab()
        navigate(url)

        image = "google_search.png"
        if exists(image, 10):
            close_tab()
            waitVanish(image, 10)
            undo_close_tab()
            if exists(image, 10):
                result = "PASS"
            else:
                result = "FAIL"
        else:
            result = "FAIL"

        print result
