# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Download links can be copied via drag & drop/context menu.'
        self.test_case_id = '99490'
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
        # Perform some downloads.
        download_files_list = [DownloadFiles.SMALL_FILE_20MB, DownloadFiles.SMALL_FILE_10MB,
                               DownloadFiles.EXTRA_SMALL_FILE_5MB]

        navigate('https://www.thinkbroadband.com/download')
        scroll_down(20)

        for pattern in download_files_list:
            download_file(pattern, DownloadFiles.OK)
            click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

        # Open the Downloads Panel.
        expected = exists(NavBar.DOWNLOADS_BUTTON_BLUE, 30)
        assert_true(self, expected, '\'Downloads\' button found.')
        click(NavBar.DOWNLOADS_BUTTON_BLUE)

        # Check that the 5MB download is complete.
        expected = exists(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED, 10)
        assert_true(self, expected, 'The 5MB download is complete.')

        expected = exists(DownloadFiles.DOWNLOAD_FILE_NAME_10MB, 10)
        assert_true(self, expected, 'The 10MB file found in the download manager.')

        # Drag and drop the 10MB file from download manager in to the tab bar.
        drag_drop(DownloadFiles.DOWNLOAD_FILE_NAME_10MB, Location(400, 30))

        try:
            wait(DownloadFiles.OK, 5)
            logger.debug('The download dialog is triggered in the page.')
            click_window_control('close')
            time.sleep(DEFAULT_UI_DELAY_LONG)
        except FindError:
            raise FindError('The download dialog is not triggered in the page.')

        # Right click on another download and select 'Copy Download Link'.
        click(NavBar.DOWNLOADS_BUTTON)
        expected = exists(DownloadFiles.DOWNLOAD_FILE_NAME_20MB, 10)
        assert_true(self, expected, 'The 20MB file found in the download manager.')

        right_click(DownloadFiles.DOWNLOAD_FILE_NAME_20MB)
        click(DownloadManager.DownloadsContextMenu.COPY_DOWNLOAD_LINK)

        new_tab()
        select_location_bar()
        edit_paste()
        type(Key.ENTER)

        try:
            wait(DownloadFiles.OK, 5)
            logger.debug('The download dialog is triggered in the page.')
            click_window_control('close')
            time.sleep(DEFAULT_UI_DELAY)
        except FindError:
            raise FindError('The download dialog is not triggered in the page.')

    def teardown(self):
        downloads_cleanup()
