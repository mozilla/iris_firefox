# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test of the \'About Firefox\' window controls'
        # Temporarily disabled due to issue #509
        self.exclude = Platform.MAC

    def run(self):
        firefox_in_about = 'firefox_in_about.png'

        # Helper function in general.py
        open_about_firefox()
        expected_1 = exists(firefox_in_about, 10)
        assert_true(self, expected_1, '\'About Firefox\' window was opened successfully.')
        # Helper function in general.py
        close_auxiliary_window()
        try:
            expected_2 = waitVanish(firefox_in_about, 10)
            assert_true(self, expected_2, '\'About Firefox\' window was closed successfully.')
        except:
            raise FindError('About Firefox\' window is still open')
