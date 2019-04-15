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
        self.set_profile_pref({'browser.warnOnQuit': True,
                               'browser.tabs.warnOnClose': True})

    def run(self):
        close_multiple_tabs_warning_pattern = Pattern('close_multiple_tabs_warning.png')

        if Settings.is_linux():
            maximize_button_pattern = Pattern('maximize_button.png')
            restore_button_pattern = Pattern('restore_button.png')

        new_window()

        new_tab()

        navigate(LocalWeb.FOCUS_TEST_SITE)

        test_site_opened = exists(LocalWeb.FOCUS_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, test_site_opened, 'Test site is opened')

        close_window()

        close_multiple_tabs_warning_exists = exists(close_multiple_tabs_warning_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, close_multiple_tabs_warning_exists, 'Close multiple tabs warning is displayed')

        if Settings.is_linux():
            maximize_button_exists = exists(maximize_button_pattern)
            assert_true(self, maximize_button_exists, 'Maximize button is displayed')

            click(maximize_button_pattern)

            hover_reg = Location(0, 0)

            hover(hover_reg)

            restore_button_exists = exists(restore_button_pattern)
            assert_true(self, restore_button_exists, 'Restore button is displayed')

            click(restore_button_pattern)

        if not Settings.is_mac():
            close_window_control('auxiliary')

            try:
                warning_vanished = wait_vanish(close_multiple_tabs_warning_pattern, Settings.FIREFOX_TIMEOUT)
                assert_true(self, warning_vanished, 'Close multiple tabs warning is dismissed after the click on the '
                                                    'Close button')
            except FindError:
                raise FindError('Close multiple tabs warning isn\'t dismissed.The Close button didn\'t works as '
                                'intended')

            close_window()

            close_multiple_tabs_warning_exists = exists(close_multiple_tabs_warning_pattern,
                                                        Settings.SHORT_FIREFOX_TIMEOUT)
            assert_true(self, close_multiple_tabs_warning_exists, 'Close multiple tabs warning is displayed')

        click_cancel_button()

        try:
            warning_vanished = wait_vanish(close_multiple_tabs_warning_pattern, Settings.FIREFOX_TIMEOUT)
            assert_true(self, warning_vanished, 'Close multiple tabs warning is dismissed after the click on the Cancel'
                                                ' button')
        except FindError:
            raise FindError('Close multiple tabs warning isn\'t dismissed.The Cancel button didn\'t works as '
                            'intended')

        close_window()

        close_multiple_tabs_warning_exists = exists(close_multiple_tabs_warning_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, close_multiple_tabs_warning_exists, 'Close multiple tabs warning is displayed')

        click(close_multiple_tabs_warning_pattern)

        try:
            warning_vanished = wait_vanish(close_multiple_tabs_warning_pattern, Settings.FIREFOX_TIMEOUT)
            window_closed = wait_vanish(LocalWeb.FOCUS_LOGO, Settings.FIREFOX_TIMEOUT)
            assert_true(self, warning_vanished and window_closed, 'The browser was closed successfully after the click '
                                                                  'on the Close Tab button')
        except FindError:
            raise FindError('The browser was not closed successfully. The Close Tab button didn\'t works as '
                            'intended')
