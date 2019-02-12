# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '\'Show all downloads states\' with no download items.'
        self.test_case_id = '99503'
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

        download_files_list = [DownloadFiles.VERY_LARGE_FILE_1GB, DownloadFiles.EXTRA_LARGE_FILE_512MB,
                               DownloadFiles.MEDIUM_FILE_100MB, DownloadFiles.EXTRA_SMALL_FILE_5MB]

        navigate('https://www.thinkbroadband.com/download')

        scroll_down(5)
        for f in download_files_list:

            download_file(f, DownloadFiles.OK)
            file_index = download_files_list.index(f)

            if file_index != 0:
                click(NavBar.DOWNLOADS_BUTTON)

            expected = exists(DownloadManager.DownloadState.PROGRESS, 10)
            assert_true(self, expected, 'Progress information is displayed.')
            expected = exists(DownloadManager.DownloadState.SPEED_PER_SECOND, 10)
            assert_true(self, expected, 'Speed information is displayed.')

            if file_index == 0:
                expected = exists(DownloadFiles.TOTAL_DOWNLOAD_SIZE_1GB, 10)
                assert_true(self, expected, 'Total size information is displayed for 1 GB file.')

            if file_index == 1:
                expected = exists(DownloadFiles.TOTAL_DOWNLOAD_SIZE_512MB, 10)
                assert_true(self, expected, 'Total size information is displayed for 512 MB file.')

            if file_index == 2:
                expected = exists(DownloadFiles.TOTAL_DOWNLOAD_SIZE_100MB, 10)
                assert_true(self, expected, 'Total size information is displayed for 100 MB file.')

            click(NavBar.DOWNLOADS_BUTTON.target_offset(-50, 0))

        click(NavBar.DOWNLOADS_BUTTON)
        expected = exists(DownloadFiles.DOWNLOAD_FILE_NAME_5MB, 10)
        assert_true(self, expected, '5MB file was downloaded.')
        expected = exists(DownloadManager.DownloadState.COMPLETED, 10)
        assert_true(self, expected, 'Download completed information is displayed.')

        # Close download panel.
        click(NavBar.DOWNLOADS_BUTTON.target_offset(-50, 0))

        # Cancel all in progress downloads.
        for step in cancel_in_progress_downloads_from_the_library():
            assert_true(self, step.resolution, step.message)

        #
        click(NavBar.DOWNLOADS_BUTTON)
        expected = Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.CANCELED.similar(0.9), 10) or \
                   Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.COMPLETED.similar(0.9), 10)
        while expected:
            remove_file_pattern = DownloadManager.DownloadState.CANCELED if \
                Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.CANCELED.similar(0.9), 10) else \
                DownloadManager.DownloadState.COMPLETED

            right_click(remove_file_pattern)
            assert_true(self, expected, 'Remove downloaded item.')

            click(DownloadManager.DownloadsContextMenu.REMOVE_FROM_HISTORY)
            expected = Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.CANCELED.similar(0.9), 10) or \
                       Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.COMPLETED.similar(0.9), 10)

        # Check that the Downloads Library window is displayed.
        for step in open_show_all_downloads_window_from_library_menu():
            assert_true(self, step.resolution, step.message)

        click_window_control('close')

    def teardown(self):
        # Remove downloads folder
        downloads_cleanup()
