# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The user is prompted when trying to close the browser while downloading files.'
        self.test_case_id = '99492'
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
        assert_true(self, expected, '\'Cancel all downloads?\' warming pop-up is displayed.')

        # Dismiss warming pop-up.
        type(text=Key.ESC)

    def teardown(self):
        # Cancel all 'in progress' downloads.
        for step in cancel_in_progress_downloads_from_the_library():
            assert_true(self, step.resolution, step.message)

        downloads_cleanup()
