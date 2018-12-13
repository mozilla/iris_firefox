# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.api.helpers.download_manager_utils import download_file, DownloadFiles, downloads_cleanup
from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open download folder.'
        self.test_case_id = '99480'
        self.test_suite_id = '1827'
        self.locales = ['en-US']
        self.exclude = Platform.LINUX
        self.blocked_by = '1513494'

    def run(self):
        navigate('https://www.thinkbroadband.com/download')

        # Download a small file.
        download_file(DownloadFiles.EXTRA_SMALL_FILE_5MB, DownloadFiles.OK)

        expected = exists(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Downloads button found.')

        expected = exists(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED, 10)
        assert_true(self, expected, 'Small size file download is completed.')

        expected = exists(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Containing folder button is available.')

        # Navigate to Downloads folder.
        click(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER)

        expected = exists(DownloadManager.DOWNLOADS_FOLDER, 10)
        assert_true(self, expected, 'Downloads folder is displayed.')

        expected = exists(DownloadFiles.FOLDER_VIEW_5MB_HIGHLIGHTED, 10)
        assert_true(self, expected, 'Downloaded file is highlighted.')

        # Close download folder window.
        click_window_control('close')

        # Switch the focus on firefox browser.
        click(NavBar.DOWNLOADS_BUTTON.target_offset(-70, 15))

        # Delete the file downloaded above.
        downloads_cleanup('5MB.zip')
