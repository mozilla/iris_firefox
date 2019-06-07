# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='This is a test of the \'Confirm close multiple tabs\' window controls',
        locale=['en-US'],
        test_case_id='120468',
        test_suite_id='1998',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.warnOnQuit': True,
                     'browser.tabs.warnOnClose': True}
    )
    def run(self, firefox):
        close_multiple_tabs_warning_pattern = Pattern('close_multiple_tabs_warning.png')
        home_button_pattern = NavBar.HOME_BUTTON

        new_tab()
        close_window()

        assert exists(close_multiple_tabs_warning_pattern, 10), 'Close multiple tabs warning was displayed successfully'
        if OSHelper.is_mac():
            click(Pattern('cancel_multiple_tabs_warning.png'))
        else:
            click_window_control('close')

        try:
            assert wait_vanish(close_multiple_tabs_warning_pattern, 10) and exists(home_button_pattern, 10),\
                'Close multiple tabs warning was canceled successfully.'
        except FindError:
            raise FindError('Close multiple tabs warning was not canceled successfully.')

        close_window()

        if OSHelper.is_linux():
            maximize_window()
            hover(Pattern('close_multiple_tabs_warning_logo.png').target_offset(0, -100), align=Alignment.TOP_LEFT)
            assert exists(MainWindow.RESIZE_BUTTON, 10), 'Close multiple tabs warning was maximized successfully.'

            minimize_window()
            assert exists(Pattern('maximize_button.png'), 10), 'Close multiple tabs warning was restored successfully.'

        assert exists(close_multiple_tabs_warning_pattern, 10), 'Close multiple tabs warning was displayed successfully'
        click(close_multiple_tabs_warning_pattern)
        try:
            assert wait_vanish(close_multiple_tabs_warning_pattern, 10) and wait_vanish(home_button_pattern, 10), \
                'The browser was closed successfully.'
        except FindError:
            raise FindError('The browser was not closed successfully.')
