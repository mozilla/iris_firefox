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
        first_bytes_label_pattern = Pattern('724_bytes_label.png')
        second_bytes_label_pattern = Pattern('163_bytes_label.png')
        about_downloads_label_pattern = Pattern('about_downloads_label.png')

        new_private_window()
        private_browsing_window_opened = exists(private_browsing_icon_pattern, 5)
        assert_true(self, private_browsing_window_opened, 'Private Browsing Window opened')

        navigate(LocalWeb.SAMPLE_FILES + '1.zip')
        save_file_dialog_exists = exists(save_file_radiobutton_pattern, 10)
        assert_true(self, save_file_dialog_exists, 'Save file dialog opened')
        click(save_file_radiobutton_pattern)
        ok_button_exists = exists(ok_save_file_button_pattern, 5)
        assert_true(self, ok_button_exists, 'Button OK exists')
        click(ok_save_file_button_pattern)
        type(Key.ESC)
        time.sleep(1)

        navigate(LocalWeb.SAMPLE_FILES + '2.zip')
        save_file_dialog_exists = exists(save_file_radiobutton_pattern, 10)
        assert_true(self, save_file_dialog_exists, 'Save file dialog opened')
        click(save_file_radiobutton_pattern)
        ok_button_exists = exists(ok_save_file_button_pattern, 5)
        assert_true(self, ok_button_exists, 'Button OK exists')
        click(ok_save_file_button_pattern)

        open_downloads()

        about_downloads_label_exists = exists(about_downloads_label_pattern, 5)
        assert_true(self, about_downloads_label_exists, 'Downloads opened')

        first_file_downloaded = exists(first_bytes_label_pattern, 5)
        assert_true(self, first_file_downloaded, 'First file saved')

        second_file_downloaded = exists(second_bytes_label_pattern, 5)
        assert_true(self, second_file_downloaded, 'Second file saved')

