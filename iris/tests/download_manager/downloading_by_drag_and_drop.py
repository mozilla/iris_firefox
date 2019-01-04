# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Downloading by Drag & Drop.'
        self.test_case_id = '108006'
        self.test_suite_id = '1827'
        self.locales = ['en-US']

    def run(self):
        # Enable the download button in the nav bar.
        auto_hide_download_button()

        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Downloads button successfully activated in the nav bar.')

        navigate('https://www.thinkbroadband.com/download')

        max_attempts = 10
        while max_attempts > 0:
            scroll_down(5)
            if exists(DownloadFiles.VERY_LARGE_FILE_1GB, 2):
                # Wait a moment to ensure button can be grabbed for drag operation
                time.sleep(Settings.UI_DELAY)
                drag_drop(DownloadFiles.VERY_LARGE_FILE_1GB, NavBar.DOWNLOADS_BUTTON, 2)
                max_attempts = 0
            max_attempts -= 1

        expected = exists(DownloadFiles.DOWNLOAD_FILE_NAME_1GB, 10)
        assert_true(self, expected, 'The downloaded file name is properly displayed in the Downloads panel.')

        # Cancel the download.
        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL, 10)
        assert_true(self, expected, 'The \'X\' button is found in the Downloads panel.')

        click(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL)
