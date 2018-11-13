# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test of the \'About Firefox\' window controls'
        self.test_case_id = '120465'
        self.test_suite_id = '1998'
        self.locales = Settings.LOCALES

    def run(self):
        firefox_in_about_pattern = Pattern('firefox_in_about.png')

        open_about_firefox()
        expected_1 = exists(firefox_in_about_pattern, 10)
        assert_true(self, expected_1, '\'About Firefox\' window was opened successfully.')

        click_window_control('close')
        try:
            expected_2 = wait_vanish(firefox_in_about_pattern, 10)
            assert_true(self, expected_2, '\'About Firefox\' window was closed successfully.')
        except FindError:
            raise FindError('About Firefox\' window is still open')
