# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from iris.api.core import mouse
from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The download can be paused/unpaused.'
        self.test_case_id = '99471'
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
        file_to_download = DownloadFiles.MEDIUM_FILE_50MB
        navigate('https://www.thinkbroadband.com/download')

        scroll_down(15)
        download_file(file_to_download, DownloadFiles.OK)

        expected = exists(DownloadManager.DownloadState.PROGRESS, 10)
        assert_true(self, expected, 'Progress information is displayed.')

        right_click(DownloadManager.DownloadState.PROGRESS)
        click(DownloadManager.DownloadsContextMenu.PAUSE)

        expected = exists(DownloadManager.DownloadState.PAUSED, 10)
        assert_true(self, expected, 'Download was paused.')

        right_click(DownloadManager.DownloadState.PAUSED)
        click(DownloadManager.DownloadsContextMenu.RESUME)

        expected = exists(DownloadManager.DownloadState.PROGRESS, 10)
        assert_true(self, expected, 'Download was resumed.')

    def teardown(self):
        # Cancel all 'in progress' downloads.
        cancel_and_clear_downloads()
        # Refocus the firefox window.
        exists(LocationBar.STAR_BUTTON_UNSTARRED, 10)
        click(LocationBar.STAR_BUTTON_UNSTARRED.target_offset(+30, 0))

        downloads_cleanup()
