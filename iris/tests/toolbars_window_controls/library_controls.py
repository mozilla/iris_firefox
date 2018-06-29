# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test of the library window controls'

    def run(self):
        library_title = 'library_title.png'
        maximize_button = 'maximize_button.png'
        restore_button = 'restore_button.png'
        library_restore_button = 'library_restore_button.png'
        library_maximize_button = 'library_maximize_button.png'

        time.sleep(1)
        open_library()
        time.sleep(1)

        expected_1 = exists(library_title, 10)
        assert_true(self, expected_1, 'The library was opened successfully')

        if Settings.getOS() == Platform.MAC:
            #maximize_auxiliary_window()
            click_auxiliary_window_control('maximize')
            time.sleep(1)

            #minimize_auxiliary_window()
            click_auxiliary_window_control('minimize')
            time.sleep(1)

        else:
            maximize_window()
            time.sleep(1)
            if Settings.getOS() == Platform.WINDOWS:
                expected_2 = exists(library_restore_button, 10)
            else:
                expected_2 = exists(restore_button, 10)
            assert_true(self, expected_2, 'The library was maximized successfully')

            minimize_window()
            time.sleep(1)
            if Settings.getOS() == Platform.WINDOWS:
                expected_3 = exists(library_maximize_button, 10)
            else:
                expected_3 = exists(maximize_button, 10)
            assert_true(self, expected_3, 'The library was restored successfully')

        minimize_window()
        time.sleep(1)

        try:
            expected_4 = waitVanish(library_title, 10)
            assert_true(self, expected_4, 'Window successfully minimized')
        except:
            raise FindError('Window not minimized, aborting test')

        if Settings.getOS() == Platform.MAC:
            open_library()

        else:
            restore_window_from_taskbar()

        expected_5 = exists(library_title, 10)
        assert_true(self, expected_5, 'The library was restored successfully')

        #close_auxiliary_window()
        click_auxiliary_window_control('close')
        try:
            expected_6 = waitVanish(library_title, 10)
            assert_true(self, expected_6, 'The library was closed successfully')
        except:
            raise FindError('The library didn\'t close successfully')
