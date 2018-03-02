# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.



from test_case import *


class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is just a sample test for keyboard shortcuts"


    def run(self):

        # wait a bit so I can manually setup browser for shortcut under test
        sleep(10)

        # run the keyboard shortcut
        open_file_picker()

        # wait a bit to get visual confirmation
        sleep (5)
