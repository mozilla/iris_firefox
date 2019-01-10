# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The user is prompted when trying to close the private window mode while downloading files.'
        self.test_case_id = '99823'
        self.test_suite_id = '1827'
        self.locales = ['en-US']

    def run(self):
        new_private_window()
        expected = exists(PrivateWindow.private_window_pattern, 10)
        assert_true(self, expected, 'Private window successfully loaded.')

        download_files_list = [DownloadFiles.VERY_LARGE_FILE_1GB, DownloadFiles.EXTRA_LARGE_FILE_512MB]

        navigate('https://www.thinkbroadband.com/download')

        scroll_down(5)
        for pattern in download_files_list:
            download_file(pattern, DownloadFiles.OK)
            click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON)
        expected = exists(DownloadFiles.TOTAL_DOWNLOAD_SIZE_1GB, 10)
        assert_true(self, expected, 'The 1GB download is in progress.')

        expected = exists(DownloadFiles.TOTAL_DOWNLOAD_SIZE_512MB, 10)
        assert_true(self, expected, 'The 512MB download is in progress.')

        quit_firefox()

        expected = exists(DownloadFiles.CANCEL_ALL_DOWNLOADS_POP_UP, 10)
        assert_true(self, expected, '\'Cancel all downloads?\' warning pop-up is displayed.')

        # Dismiss warning pop-up.
        type(text=Key.ESC)

    def teardown(self):
        # Open the 'Show Downloads' window and cancel all 'in progress' downloads.
        for step in show_all_downloads_from_library_menu_private_window():
            assert_true(self, step.resolution, step.message)

        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL, 10)
        assert_true(self, expected, 'The \'X\' button is found.')
        while expected:
            click(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL)
            expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL, 10)

        close_tab()
        close_tab()
