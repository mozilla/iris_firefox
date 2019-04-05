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
        # self.profile = Profile.BRAND_NEW
        self.set_profile_pref({'browser.warnOnQuit': True,
                               'browser.tabs.warnOnClose': True})

    def run(self):
        close_multiple_tabs_warning_pattern = Pattern('close_multiple_tabs_warning.png')

        if Settings.is_mac():
            cancel_multiple_tabs_warning_pattern = Pattern('cancel_multiple_tabs_warning.png')

        if Settings.is_linux():
            close_multiple_tabs_warning_logo_pattern = Pattern('close_multiple_tabs_warning_logo.png')
            maximize_button_pattern = Pattern('maximize_button.png')
            restore_button_pattern = Pattern('restore_button.png')

        new_window()

        new_tab()

        navigate(LocalWeb.FOCUS_TEST_SITE)

        test_site_opened = exists(LocalWeb.FOCUS_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, test_site_opened, 'test_site_opened')

        close_window()

        close_multiple_tabs_warning_exists = exists(close_multiple_tabs_warning_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, close_multiple_tabs_warning_exists, 'close_multiple_tabs_warning_exists')

        click_cancel_button()

        close_window()

        close_window_control('auxiliary')

        close_window()

        close_multiple_tabs_warning_exists = exists(close_multiple_tabs_warning_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, close_multiple_tabs_warning_exists, 'close_multiple_tabs_warning_exists')

        click(close_multiple_tabs_warning_pattern)

        try:
            expected_7 = wait_vanish(close_multiple_tabs_warning_pattern, Settings.FIREFOX_TIMEOUT)
            expected_8 = wait_vanish(LocalWeb.FOCUS_LOGO, Settings.FIREFOX_TIMEOUT)
            assert_true(self, expected_7 and expected_8, 'The browser was closed successfully')
        except FindError:
            raise FindError('The browser was not closed successfully')
