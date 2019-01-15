# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Notifications are displayed if downloads are finished or new ones initiated.'
        self.test_case_id = '99493'
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
        navigate('https://www.thinkbroadband.com/download')

        scroll_down(15)
        if Settings.get_os() == Platform.LINUX:
            download_file(DownloadFiles.MEDIUM_FILE_50MB, DownloadFiles.OK)
        else:
            download_file(DownloadFiles.SMALL_FILE_20MB, DownloadFiles.OK)

        expected = exists(DownloadManager.DownloadState.PROGRESS, 10)
        assert_true(self, expected, 'Progress information is displayed.')
        expected = exists(DownloadManager.DownloadState.SPEED_PER_SECOND, 10)
        assert_true(self, expected, 'Speed information is displayed.')

        # Download a second file to check the blue download arrow
        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))
        download_file(DownloadFiles.EXTRA_SMALL_FILE_5MB, DownloadFiles.OK)
        expected = exists(NavBar.DOWNLOADS_BUTTON_BLUE, 10)
        assert_true(self, expected, 'Downloads button found.')

    def teardown(self):
        # Cancel all 'in progress' downloads.
        cancel_and_clear_downloads()
        # Refocus the firefox window.
        exists(LocationBar.STAR_BUTTON_UNSTARRED, 10)
        click(LocationBar.STAR_BUTTON_UNSTARRED.target_offset(+30, 0))

        downloads_cleanup()
