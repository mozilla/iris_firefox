# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Download Manager Smoke.'
        self.test_case_id = '99157'
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
        navigate('https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-central/')

        download_file(DownloadFiles.FIREFOX_INSTALLER.similar(0.85), DownloadFiles.OK)

        expected = exists(DownloadManager.DownloadState.COMPLETED, 90)
        assert_true(self, expected, 'Firefox installer download is completed.')

        expected = exists(DownloadManager.DownloadsPanel.OPEN_DOWNLOAD_FOLDER, 10)
        assert_true(self, expected, 'Containing folder button is available.')

        # Navigate to Downloads folder.
        click(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER)

        if Settings.get_os() == Platform.LINUX:
            click(Pattern('linux_folder_icon.png'))

        expected = exists(DownloadManager.DOWNLOADS_FOLDER, 10)
        assert_true(self, expected, 'Downloads folder is displayed.')

        expected = exists(DownloadFiles.FIREFOX_INSTALLER_HIGHLIGHTED, 10)
        assert_true(self, expected, 'Firefox installer is displayed in downloads folder.')

        click_window_control('close')

        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Download button found in the page.')

        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

    def teardown(self):
        downloads_cleanup()
