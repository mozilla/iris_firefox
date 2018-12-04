# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Downloaded files from Private session are successfully saved locally'
        self.test_case_id = '101676'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def run(self):

        private_browsing_icon_pattern = Pattern('private_browsing_icon.png')
        save_file_radiobutton_pattern = Pattern('save_file_radiobutton.png')
        ok_save_file_button_pattern = Pattern('ok_save_file_button.png')
        stay_in_private_browsing_button_pattern = Pattern('stay_in_private_browsing_button.png')
        cancel_one_download_button_pattern = Pattern('cancel_one_download_button.png')

        new_private_window()
        private_browsing_window_opened = exists(private_browsing_icon_pattern, 5)
        assert_true(self, private_browsing_window_opened, 'Private Browsing Window opened')

        navigate('https://www.sample-videos.com/text/Sample-text-file-10kb.txt')
        save_file_dialog_exists = exists(save_file_radiobutton_pattern, 10)
        assert_true(self, save_file_dialog_exists, 'Save file dialog opened')
        click(save_file_radiobutton_pattern)
        ok_button_exists = exists(ok_save_file_button_pattern, 5)
        assert_true(self, ok_button_exists, 'Button OK exists')
        click(ok_save_file_button_pattern)

        navigate('https://www.sample-videos.com/text/Sample-text-file-20kb.txt')
        save_file_dialog_exists = exists(save_file_radiobutton_pattern, 10)
        assert_true(self, save_file_dialog_exists, 'Save file dialog opened')
        click(save_file_radiobutton_pattern)
        ok_button_exists = exists(ok_save_file_button_pattern, 5)
        assert_true(self, ok_button_exists, 'Button OK exists')
        click(ok_save_file_button_pattern)


        # handle linux save progress popup

        if Settings.is_linux():
            time.sleep(5)
            type(Key.ESC)

        close_tab()

        stay_in_private_browsing_button_exists = exists(stay_in_private_browsing_button_pattern, 5)
        assert_true(self, stay_in_private_browsing_button_exists, 'The Cancel All Downloads dialog is opened')

        click(stay_in_private_browsing_button_pattern)

        try:
            dialog_dismissed = wait_vanish(stay_in_private_browsing_button_pattern, 5)
            assert_true(self, dialog_dismissed, 'The dialog is dismissed')
        except FindError:
            raise FindError('The dialog is not dismissed')

        close_tab()

        cancel_one_download_button_exists = exists(cancel_one_download_button_pattern, 5)
        assert_true(self, cancel_one_download_button_exists, 'Cancel button exists')

        click(cancel_one_download_button_pattern)

        try:
            private_window_closed = wait_vanish(private_browsing_icon_pattern, 5)
            assert_true(self, private_window_closed, 'Private window is dismissed')
        except FindError:
            raise FindError('Private window is not dismissed')
