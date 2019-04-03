# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.api.core import mouse
from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Clear download preview panel.'
        self.test_case_id = '99482'
        self.test_suite_id = '1827'
        self.locales = ['en-US']

    def setup(self):
        """T
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

        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        download_file(file_to_download, DownloadFiles.OK)

        expected = exists(DownloadManager.DownloadState.COMPLETED, 10)
        assert_true(self, expected, 'Completed information is displayed.')

        right_click(DownloadManager.DownloadState.COMPLETED)
        click(DownloadManager.DownloadsContextMenu.CLEAR_PREVIEW_PANEL)

        # Enable the download button in the nav bar.
        auto_hide_download_button()

        # Check that all of the downloads were cleared.
        expected = exists(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Downloads button has been found.')
        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON)
        expected = exists(DownloadManager.DownloadsPanel.NO_DOWNLOADS_FOR_THIS_SESSION)
        assert_true(self, expected, 'All downloads were cleared.')

    def teardown(self):
        # Cancel all 'in progress' downloads.
        cancel_and_clear_downloads()
        # Refocus the firefox window.
        exists(LocationBar.STAR_BUTTON_UNSTARRED, 10)
        click(LocationBar.STAR_BUTTON_UNSTARRED.target_offset(+30, 0))
        downloads_cleanup()
