# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='This is a test of the \'Confirm close multiple tabs\' window controls',
        locale=Locales.ENGLISH,
        test_case_id='120468',
        test_suite_id='1998',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.warnOnQuit': True,
                     'browser.tabs.warnOnClose': True}
    )
    def test_run(self, firefox):
        close_multiple_tabs_warning_pattern = Pattern('close_multiple_tabs_warning.png')
        home_button_pattern = NavBar.HOME_BUTTON

        new_tab()
        close_window()

        expected_1 = exists(close_multiple_tabs_warning_pattern, 10)
        assert expected_1, 'Close multiple tabs warning was displayed successfully.'
        if OSHelper.is_mac():
            click(Pattern('cancel_multiple_tabs_warning.png'))
        else:
            click_window_control('close')

        try:
            expected_2 = wait_vanish(close_multiple_tabs_warning_pattern, 10)
            expected_3 = exists(home_button_pattern, 10)
            assert expected_2 and expected_3, 'Close multiple tabs warning was canceled successfully.'
        except FindError:
            raise FindError('Close multiple tabs warning was not canceled successfully.')

        close_window()

        if OSHelper.is_linux():
            maximize_window()
            hover(Pattern('close_multiple_tabs_warning_logo.png').target_offset(0, -100), align=Alignment.TOP_LEFT)
            expected_4 = exists(Pattern('maximize_button.png'), 10)
            assert expected_4, 'Close multiple tabs warning was maximized successfully.'

            minimize_window()
            expected_5 = exists(Pattern('maximize_button.png'), 10)
            assert expected_5, 'Close multiple tabs warning was restored successfully.'

        expected_6 = exists(close_multiple_tabs_warning_pattern, 10)
        assert expected_6, 'Close multiple tabs warning was displayed successfully.'
        click(close_multiple_tabs_warning_pattern)
        try:
            expected_7 = wait_vanish(close_multiple_tabs_warning_pattern, 10)
            expected_8 = wait_vanish(home_button_pattern, 10)
            assert expected_7 and expected_8, 'The browser was closed successfully.'
        except FindError:
            raise FindError('The browser was not closed successfully.')
