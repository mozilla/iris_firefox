# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test of the \'Confirm close multiple tabs\' window controls'
        self.test_case_id = '120468'
        self.test_suite_id = '1998'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        self.set_profile_pref({'browser.warnOnQuit': True,
                               'browser.tabs.warnOnClose': True})

    def run(self):
        close_multiple_tabs_warning_pattern = Pattern('close_multiple_tabs_warning.png')
        home_button_pattern = NavBar.HOME_BUTTON

        if Settings.is_mac():
            cancel_multiple_tabs_warning_pattern = Pattern('cancel_multiple_tabs_warning.png')

        if Settings.is_linux():
            close_multiple_tabs_warning_logo_pattern = Pattern('close_multiple_tabs_warning_logo.png')
            maximize_button_pattern = Pattern('maximize_button.png')
            restore_button_pattern = Pattern('restore_button.png')

        new_tab()

        close_window()

        expected_1 = exists(close_multiple_tabs_warning_pattern, 10)
        assert_true(self, expected_1, 'Close multiple tabs warning was displayed successfully')
        if Settings.is_mac():
            click(cancel_multiple_tabs_warning_pattern)
        else:
            click_window_control('close')

        try:
            expected_2 = wait_vanish(close_multiple_tabs_warning_pattern, 10)
            expected_3 = exists(home_button_pattern, 10)
            assert_true(self, expected_2 and expected_3, 'Close multiple tabs warning was canceled successfully')
        except FindError:
            raise FindError('Close multiple tabs warning was not canceled successfully')

        close_window()

        if Settings.is_linux():
            maximize_window()
            hover(close_multiple_tabs_warning_logo_pattern.target_offset(0, -100))
            expected_4 = exists(restore_button_pattern, 10)
            assert_true(self, expected_4, 'Close multiple tabs warning was maximized successfully')

            minimize_window()
            expected_5 = exists(maximize_button_pattern, 10)
            assert_true(self, expected_5, 'Close multiple tabs warning was restored successfully')

        expected_6 = exists(close_multiple_tabs_warning_pattern, 10)
        assert_true(self, expected_6, 'Close multiple tabs warning was displayed successfully')
        click(close_multiple_tabs_warning_pattern)
        try:
            expected_7 = wait_vanish(close_multiple_tabs_warning_pattern, 10)
            expected_8 = wait_vanish(home_button_pattern, 10)
            assert_true(self, expected_7 and expected_8, 'The browser was closed successfully')
        except FindError:
            raise FindError('The browser was not closed successfully')
