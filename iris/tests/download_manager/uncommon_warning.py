# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Uncommon warning.'
        self.test_case_id = '107720'
        self.test_suite_id = '1827'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        self.set_profile_pref({'browser.download.dir': IrisCore.get_downloads_dir()})
        self.set_profile_pref({'browser.download.folderList': 2})
        self.set_profile_pref({'browser.download.useDownloadDir': True})
        return

    def run(self):
        uncommon_file_download_library = Pattern('uncommon_file_download_library.png')

        navigate('https://testsafebrowsing.appspot.com')

        expected = exists(DownloadFiles.UNCOMMON, 10)
        assert_true(self, expected, 'Uncommon file has been found.')

        width, height = DownloadFiles.UNCOMMON.get_size()
        download_file(DownloadFiles.UNCOMMON.target_offset(width + 10, height / 2), DownloadFiles.OK)

        expected = exists(DownloadManager.DownloadsPanel.UNCOMMON_DOWNLOAD_ICON, 10)
        assert_true(self, expected, 'Uncommon download icon is displayed.')

        expected = exists(DownloadManager.DownloadsPanel.UNCOMMON_DOWNLOAD, 10)
        assert_true(self, expected, 'Uncommon message is displayed.')

        click(DownloadManager.DownloadsPanel.ADD_REMOVE_DOWNLOADS_ARROW)

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.HEADER, 10)
        assert_true(self, expected, 'Download details header is displayed.')

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.UNCOMMON_DOWNLOAD_TITLE, 10)
        assert_true(self, expected, 'Download details title is displayed.')

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.UNCOMMON_DETAILS_1, 10)
        assert_true(self, expected, 'Download details 1 are displayed.')

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.BLOCKED_DETAILS_2, 10)
        assert_true(self, expected, 'Download details 2 are displayed.')

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.UNWANTED_BADGE, 10)
        assert_true(self, expected, 'Download details uncommon icon is displayed.')

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.OPEN_FILE_BUTTON, 10)
        assert_true(self, expected, 'Open file button is displayed.')

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.REMOVE_FILE_BUTTON, 10)
        assert_true(self, expected, 'Remove file button is displayed.')

        # Open the uncommon file.
        if Settings.get_os() == Platform.MAC:
            uncommon_file = Pattern('uncommon_file_name.png')
            click(DownloadManager.DownloadsPanel.DownloadDetails.OPEN_FILE_BUTTON)
            expected = exists(uncommon_file, 10)
            assert_true(self, expected, 'Uncommon file is displayed.')
            click_window_control('close')
            click(NavBar.DOWNLOADS_BUTTON)
            right_click(DownloadManager.DownloadState.COMPLETED)
        else:
            click(DownloadManager.DownloadsPanel.DownloadDetails.DOWNLOADS_BACK_ARROW)
            right_click(DownloadManager.DownloadsPanel.UNCOMMON_DOWNLOAD)

        # Clear the download panel.
        click(DownloadManager.DownloadsContextMenu.REMOVE_FROM_HISTORY)

        # Check the uncommon download button.
        download_file(DownloadFiles.UNCOMMON.target_offset(width + 10, height / 2), DownloadFiles.OK)
        expected = exists(NavBar.UNWANTED_DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Uncommon downloads button is displayed.')

        # Remove the file from the download panel.
        click(NavBar.UNWANTED_DOWNLOADS_BUTTON)
        click(DownloadManager.DownloadsPanel.ADD_REMOVE_DOWNLOADS_ARROW)
        click(DownloadManager.DownloadsPanel.DownloadDetails.REMOVE_FILE_BUTTON)

        # Check that there are no downloads displayed in Downloads Library window.
        for step in open_show_all_downloads_window_from_library_menu():
            assert_true(self, step.resolution, step.message)

        expected = exists(uncommon_file_download_library, 10)
        assert_false(self, expected, 'Uncommon file was deleted from Downloads Library.')
        click_window_control('close')

        # Check that there are no downloads displayed in the 'about:downloads' page.
        navigate('about:downloads')
        expected = exists(DownloadManager.AboutDownloads.NO_DOWNLOADS, 10)
        assert_true(self, expected, 'There are no downloads displayed in the \'about:downloads\' page.')

        # Check that there are no downloads displayed in the downloads folder.
        open_directory(IrisCore.get_downloads_dir())
        expected = exists(uncommon_file_download_library, 10)
        assert_false(self, expected, 'Uncommon file was deleted from the download folder.')

        click_window_control('close')

    def teardown(self):
        click(DownloadManager.AboutDownloads.NO_DOWNLOADS)
        downloads_cleanup()
