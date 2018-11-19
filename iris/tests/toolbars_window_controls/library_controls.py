# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test of the library window controls'
        self.test_case_id = '120467'
        self.test_suite_id = '1998'
        self.locales = ['en-US']

    def run(self):

        library_title_pattern = Library.TITLE
        if Settings.get_os() == Platform.LINUX:
            restore_button_pattern = Pattern('restore_button.png')
        if Settings.get_os() == Platform.WINDOWS:
            library_restore_button_pattern = Pattern('library_restore_button.png')

        open_library()

        expected_1 = exists(library_title_pattern, 10)
        assert_true(self, expected_1, 'The library was opened successfully')

        if Settings.get_os() == Platform.MAC:
            click_window_control('maximize')
            click_window_control('minimize')
        else:
            click_window_control('maximize')
            if Settings.get_os() == Platform.WINDOWS:
                expected_2 = exists(library_restore_button_pattern, 10)
            else:
                expected_2 = exists(restore_button_pattern, 10)
            assert_true(self, expected_2, 'The library was maximized successfully')

            click_window_control('minimize')
        try:
            expected_4 = wait_vanish(library_title_pattern, 10)
            assert_true(self, expected_4, 'Window successfully minimized')
        except FindError:
            raise FindError('Window not minimized, aborting test')

        if Settings.get_os() == Platform.MAC:
            open_library()
        else:
            restore_window_from_taskbar(option='library_menu')

        expected_5 = exists(library_title_pattern, 10)
        assert_true(self, expected_5, 'The library was restored successfully')

        click_window_control('close')
        try:
            expected_6 = wait_vanish(library_title_pattern, 10)
            assert_true(self, expected_6, 'The library was closed successfully')
        except FindError:
            raise FindError('The library didn\'t close successfully')
