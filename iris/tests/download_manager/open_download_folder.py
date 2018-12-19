# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '\'Open Download Folder\' opens the folder which Firefox is set to save its downloads.'
        self.test_case_id = '99480'
        self.test_suite_id = '1827'
        self.locales = ['en-US']
        self.exclude = Platform.LINUX
        self.blocked_by = '1513494'

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

        download_file(DownloadFiles.EXTRA_SMALL_FILE_5MB, DownloadFiles.OK)

        expected = exists(NavBar.DOWNLOADS_BUTTON_BLUE, 10)
        assert_true(self, expected, 'Downloads button found.')

        expected = exists(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED, 10)
        assert_true(self, expected, 'Small size file download is completed.')

        expected = exists(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER, 10)
        assert_true(self, expected, 'Containing folder button is available.')

        # Navigate to Downloads folder.
        click(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER)

        expected = exists(DownloadManager.DOWNLOADS_FOLDER, 10)
        assert_true(self, expected, 'Downloads folder is displayed.')

        expected = exists(DownloadFiles.FOLDER_VIEW_5MB_HIGHLIGHTED, 10)
        assert_true(self, expected, 'Downloaded file is found.')

        # Close download folder window.
        close_tab()

        # Switch the focus on firefox browser.
        click(NavBar.DOWNLOADS_BUTTON.target_offset(-70, 15))

    def teardown(self):
        downloads_cleanup()
