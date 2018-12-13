# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The user is prompted for confirmation when closing a private window with active downloads'
        self.test_case_id = '101675'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def run(self):
        stay_in_private_browsing_button_pattern = Pattern('stay_in_private_browsing_button.png')
        cancel_one_download_button_pattern = Pattern('cancel_one_download_button.png')

        new_private_window()
        private_browsing_window_opened = exists(PrivateWindow.private_window_pattern, 5)
        assert_true(self, private_browsing_window_opened, 'Private Browsing Window opened')

        navigate('http://releases.ubuntu.com/14.04.4/ubuntu-14.04.4-desktop-amd64.iso?_ga=2.161399869.1280481406'
                 '.1513173033-114787657.1513173033')

        save_file_dialog_exists = exists(DownloadDialog.SAVE_FILE_RADIOBUTTON, 10)
        assert_true(self, save_file_dialog_exists, 'Save file dialog opened')

        click(DownloadDialog.SAVE_FILE_RADIOBUTTON)

        ok_button_exists = exists(DownloadDialog.OK_BUTTON, 5)
        assert_true(self, ok_button_exists, 'Button OK exists')

        click(DownloadDialog.OK_BUTTON)

        restore_firefox_focus()

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
            private_window_closed = wait_vanish(PrivateWindow.private_window_pattern, 5)
            assert_true(self, private_window_closed, 'Private window is dismissed')
        except FindError:
            raise FindError('Private window is not dismissed')
