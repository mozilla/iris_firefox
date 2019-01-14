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
        self.blocked_by = {'id': 'issue_1811', 'platform': [Platform.WINDOWS]}

    def setup(self):
        BaseTest.setup(self)
        self.set_profile_pref({'browser.download.dir': IrisCore.get_downloads_dir()})
        self.set_profile_pref({'browser.download.folderList': 2})
        self.set_profile_pref({'browser.download.useDownloadDir': True})
        downloads_cleanup()

    def teardown(self):
        downloads_cleanup()

    def run(self):
        first_bytes_label_pattern = Pattern('163_bytes_label.png')
        first_bytes_label_pattern.similar(0.7)
        second_bytes_label_pattern = Pattern('724_bytes_label.png')
        second_bytes_label_pattern.similar(0.7)
        about_downloads_label_pattern = Pattern('about_downloads_label.png')

        new_private_window()
        private_browsing_window_opened = exists(PrivateWindow.private_window_pattern, 5)
        assert_true(self, private_browsing_window_opened, 'Private Browsing Window opened')

        navigate(LocalWeb.SAMPLE_FILES + '1.zip')
        save_file_dialog_exists = exists(DownloadDialog.SAVE_FILE_RADIOBUTTON, 10)
        assert_true(self, save_file_dialog_exists, 'Save file dialog opened')

        click(DownloadDialog.SAVE_FILE_RADIOBUTTON)
        ok_button_exists = exists(DownloadDialog.OK_BUTTON, 5)
        assert_true(self, ok_button_exists, 'Button OK exists')

        click(DownloadDialog.OK_BUTTON)
        
        restore_firefox_focus()

        navigate(LocalWeb.SAMPLE_FILES + '2.zip')
        save_file_dialog_exists = exists(DownloadDialog.SAVE_FILE_RADIOBUTTON, 10)
        assert_true(self, save_file_dialog_exists, 'Save file dialog opened')

        click(DownloadDialog.SAVE_FILE_RADIOBUTTON)
        ok_button_exists = exists(DownloadDialog.OK_BUTTON, 5)
        assert_true(self, ok_button_exists, 'Button OK exists')

        click(DownloadDialog.OK_BUTTON)

        open_downloads()

        about_downloads_label_exists = exists(about_downloads_label_pattern, 5)
        assert_true(self, about_downloads_label_exists, 'Downloads opened')

        if Settings.is_mac():
            click(about_downloads_label_pattern)

        first_file_downloaded = exists(first_bytes_label_pattern, 5)
        assert_true(self, first_file_downloaded, 'First file saved')

        second_file_downloaded = exists(second_bytes_label_pattern, 5)
        assert_true(self, second_file_downloaded, 'Second file saved')

        close_window()
