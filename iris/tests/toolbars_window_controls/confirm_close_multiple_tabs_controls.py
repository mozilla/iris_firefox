# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test of the \'Confirm close multiple tabs\' window controls'

    def run(self):
        close_multiple_tabs_warning = 'close_multiple_tabs_warning.png'
        cancel_multiple_tabs_warning = 'cancel_multiple_tabs_warning.png'
        close_multiple_tabs_warning_logo = 'close_multiple_tabs_warning_logo.png'
        home_button = 'home_button.png'
        maximize_button = 'maximize_button.png'
        restore_button = 'restore_button.png'

        new_tab()
        time.sleep(1)

        close_window()

        expected_1 = exists(close_multiple_tabs_warning, 10)
        assert_true(self, expected_1, 'Close multiple tabs warning was displayed successfully')
        if get_os() == 'osx':
            click(cancel_multiple_tabs_warning)
        else:
            click_auxiliary_window_control('close')

        try:
            expected_2 = waitVanish(close_multiple_tabs_warning, 10)
            expected_3 = exists(home_button, 10)
            assert_true(self, expected_2 and expected_3, 'Close multiple tabs warning was canceled successfully')
        except:
            raise FindError('Close multiple tabs warning was not canceled successfully')

        close_window()

        if get_os() == 'linux':
            maximize_window()
            time.sleep(1)
            hover(Pattern(close_multiple_tabs_warning_logo).targetOffset(0, -100))
            expected_4 = exists(restore_button, 10)
            assert_true(self, expected_4, 'Close multiple tabs warning was maximized successfully')

            minimize_window()
            expected_5 = exists(maximize_button, 10)
            assert_true(self, expected_5, 'Close multiple tabs warning was restored successfully')

        expected_6 = exists(close_multiple_tabs_warning, 10)
        assert_true(self, expected_6, 'Close multiple tabs warning was displayed successfully')
        click(close_multiple_tabs_warning)
        try:
            expected_7 = waitVanish(close_multiple_tabs_warning, 10)
            expected_8 = waitVanish(home_button, 10)
            assert_true(self, expected_7 and expected_8, 'The browser was closed successfully')
        except:
            raise FindError('The browser was not closed successfully')
