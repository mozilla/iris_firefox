# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The number of downloads are properly truncated.'
        self.test_case_id = '99472'
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
        file_to_download = DownloadFiles.EXTRA_SMALL_FILE_5MB

        download_files_list = [DownloadFiles.VERY_LARGE_FILE_1GB, DownloadFiles.EXTRA_LARGE_FILE_512MB,
                               DownloadFiles.MEDIUM_FILE_100MB, DownloadFiles.MEDIUM_FILE_50MB,
                               DownloadFiles.SMALL_FILE_20MB]

        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        # Wait for the page to be loaded.
        try:
            wait(DownloadFiles.VERY_LARGE_FILE_1GB, 10)
            logger.debug('File is present in the page.')
        except FindError:
            raise FindError('File is not present in the page.')

        select_throttling(NetworkOption.REGULAR_4G)

        expected = exists(NavBar.RELOAD_BUTTON, 10)
        assert_true(self, expected, 'Reload button found in the page.')
        click(NavBar.RELOAD_BUTTON)

        expected = exists(DownloadFiles.STATUS_200, 10)
        assert_true(self, expected, 'Page successfully reloaded.')

        for f in download_files_list:
            download_file(f, DownloadFiles.OK)

        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Download button found in the page.')

        click(NavBar.DOWNLOADS_BUTTON)

        expected = exists(DownloadFiles.DOWNLOAD_FILE_NAME_1GB, 10)
        assert_true(self, expected, '1GB file is present in the download panel.')

        download_file(file_to_download, DownloadFiles.OK)

        click(NavBar.DOWNLOADS_BUTTON)

        expected = exists(DownloadFiles.DOWNLOAD_FILE_NAME_5MB, 10)
        assert_true(self, expected, '5MB file was downloaded.')

        expected = exists(DownloadManager.DownloadState.PROGRESS, 10)
        assert_true(self, expected, 'Progress information is displayed.')
        expected = exists(DownloadManager.DownloadState.SPEED_PER_SECOND.similar(0.75), 10)
        assert_true(self, expected, 'Speed information is displayed.')

        expected = exists(DownloadFiles.DOWNLOAD_FILE_NAME_1GB, 10)
        assert_false(self, expected, '1GB file was removed from the download panel.')

        # Close download panel.
        click(NavBar.DOWNLOADS_BUTTON.target_offset(-50, 0))

    def teardown(self):
        # Cancel all 'in progress' downloads.
        cancel_and_clear_downloads()
        # Refocus the firefox window.
        exists(LocationBar.STAR_BUTTON_UNSTARRED, 10)
        click(LocationBar.STAR_BUTTON_UNSTARRED.target_offset(+30, 0))
        downloads_cleanup()
