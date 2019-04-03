# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Hover behavior.'
        self.test_case_id = '99478'
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
        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        download_file(DownloadFiles.VERY_LARGE_FILE_1GB, DownloadFiles.OK)

        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Downloads button found.')

        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL, 10)
        assert_true(self, expected, 'The \'X\' button is properly displayed.')

        # Hover the 'X' button.
        hover(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL)
        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL_HIGHLIGHTED, 10)
        assert_true(self, expected, 'The \'X\' button is highlighted properly.')

        # Click the 'X' button.
        click(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL_HIGHLIGHTED)
        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_RETRY_HIGHLIGHTED, 10)
        assert_true(self, expected, 'The Retry button is highlighted properly.')

        expected = exists(DownloadFiles.DOWNLOAD_FILE_NAME_1GB, 10)
        assert_true(self, expected, 'The downloaded file name is properly displayed.')

        # Hover the file name.
        hover(DownloadFiles.DOWNLOAD_FILE_NAME_1GB)
        expected = exists(DownloadFiles.DOWNLOAD_CANCELED, 10)
        assert_true(self, expected, 'The status and the source page are properly displayed when hovering the downloaded'
                                    ' file name.')

    def teardown(self):
        downloads_cleanup()
