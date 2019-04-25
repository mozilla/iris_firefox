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

        download_files_list = [DownloadFiles.EXTRA_SMALL_FILE_5MB, DownloadFiles.EXTRA_LARGE_FILE_512MB,
                               DownloadFiles.MEDIUM_FILE_100MB, DownloadFiles.VERY_LARGE_FILE_1GB]

        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        # Wait for the page to be loaded.
        try:
            wait(DownloadFiles.VERY_LARGE_FILE_1GB, 10)
            logger.debug('File is present in the page.')
        except FindError:
            raise FindError('File is not present in the page.')

        select_throttling(NetworkOption.GOOD_3G)

        expected = exists(NavBar.RELOAD_BUTTON, 10)
        assert_true(self, expected, 'Reload button found in the page.')
        click(NavBar.RELOAD_BUTTON)

        expected = exists(DownloadFiles.STATUS_200, 10)
        assert_true(self, expected, 'Page successfully reloaded.')

        for f in download_files_list:

            download_file(f, DownloadFiles.OK)
            file_index = download_files_list.index(f)

            if file_index == 0:
                time.sleep(DEFAULT_SYSTEM_DELAY)
            else:
                click(NavBar.DOWNLOADS_BUTTON)

            expected = exists(DownloadManager.DownloadState.PROGRESS, 10)
            assert_true(self, expected, 'Progress information is displayed.')
            expected = exists(DownloadManager.DownloadState.SPEED_PER_SECOND, 10)
            assert_true(self, expected, 'Speed information is displayed.')

        # Close download panel.
        click(NavBar.DOWNLOADS_BUTTON.target_offset(-50, 0))

        # Cancel all in progress downloads.
        for step in cancel_in_progress_downloads_from_the_library():
            assert_true(self, step.resolution, step.message)

        #
        click(NavBar.DOWNLOADS_BUTTON)
        expected = Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.CANCELED.similar(0.9), 10) or \
                   Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.COMPLETED.similar(0.9), 10)
        remove_file_pattern = DownloadManager.DownloadState.CANCELED if \
            Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.CANCELED.similar(0.9), 5) else \
            DownloadManager.DownloadState.COMPLETED

        while expected:
            right_click(remove_file_pattern)
            assert_true(self, expected, 'Remove downloaded item.')
            click(DownloadManager.DownloadsContextMenu.REMOVE_FROM_HISTORY)

            if Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.CANCELED.similar(0.9), 5):
                expected = True
                remove_file_pattern = DownloadManager.DownloadState.CANCELED
            elif Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.COMPLETED.similar(0.9), 5):
                expected = True
                remove_file_pattern = DownloadManager.DownloadState.COMPLETED
            elif Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.FAILED.similar(0.9), 5):
                expected = True
                remove_file_pattern = DownloadManager.DownloadState.FAILED
            else:
                expected = False

        # Check that the Downloads Library window is displayed.
        for step in open_show_all_downloads_window_from_library_menu():
            assert_true(self, step.resolution, step.message)

        expected = exists(DownloadFiles.DOWNLOAD_TYPE_ICON.similar(0.95), 5) or exists(
            DownloadFiles.DOWNLOAD_TYPE_ICON_ZIP.similar(0.95), 5)
        assert_false(self, expected, 'There are no downloads displayed in Library, Downloads section.')

        click_window_control('close')

    def teardown(self):
        # Remove downloads folder
        downloads_cleanup()
