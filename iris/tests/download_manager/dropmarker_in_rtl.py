# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Dropmarker in RTL.'
        self.test_case_id = '99500'
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

        # Change firefox alignment to be Right-To-Left.
        change_preference('intl.uidirection', '2')

        # Check if main firefox buttons are aligned RTL.
        right_top_corner_region = Screen.UPPER_RIGHT_CORNER.top_half()

        expected = exists(NavBar.BACK_BUTTON_RTL, Settings.FIREFOX_TIMEOUT, right_top_corner_region)
        assert_true(self, expected, '\'Back\' button is aligned RTL.')

        expected = exists(NavBar.HOME_BUTTON, Settings.FIREFOX_TIMEOUT, right_top_corner_region)
        assert_true(self, expected, '\'Home\' button is aligned RTL.')

        expected = exists(NavBar.FORWARD_BUTTON_RTL, Settings.FIREFOX_TIMEOUT, right_top_corner_region)
        assert_true(self, expected, '\'Forward\' button is aligned RTL.')

        expected = exists(NavBar.RELOAD_BUTTON_RTL, Settings.FIREFOX_TIMEOUT, right_top_corner_region)
        assert_true(self, expected, '\'Reload\' button is aligned RTL.')

        left_top_half_region = Screen.LEFT_HALF.top_half()

        expected = exists(LocationBar.STAR_BUTTON_UNSTARRED, Settings.FIREFOX_TIMEOUT, left_top_half_region)
        assert_true(self, expected, '\'Star dialog\' button is aligned RTL.')

        expected = exists(NavBar.HAMBURGER_MENU, Settings.FIREFOX_TIMEOUT, left_top_half_region)
        assert_true(self, expected, '\'Hamburger menu\' button is aligned RTL.')

        expected = exists(NavBar.SIDEBAR_MENU_RTL, Settings.FIREFOX_TIMEOUT, left_top_half_region)
        assert_true(self, expected, '\'Sidebar\' button is aligned RTL.')

        expected = exists(NavBar.LIBRARY_MENU, Settings.FIREFOX_TIMEOUT, left_top_half_region)
        assert_true(self, expected, '\'Library Menu dialog\' button is aligned RTL.')

        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)
        download_files_list = [DownloadFiles.SMALL_FILE_20MB, DownloadFiles.SMALL_FILE_10MB,
                               DownloadFiles.EXTRA_SMALL_FILE_5MB]

        for f in download_files_list:
            download_file(f, DownloadFiles.OK)
            file_index = download_files_list.index(f)

            if file_index == 0:
                expected = exists(NavBar.DOWNLOADS_BUTTON, Settings.FIREFOX_TIMEOUT)
                assert_true(self, expected, 'Download button found in the page.')

            click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(50, 0))

        # Check if Downloads Panel details are aligned RTL,
        # containing folder icon aligned on the left and download type icon aligned on the right for each file.
        expected = exists(NavBar.DOWNLOADS_BUTTON_BLUE, Settings.SITE_LOAD_TIMEOUT, left_top_half_region)
        assert_true(self, expected, '\'Downloads\'button  button is aligned RTL.')

        click(NavBar.DOWNLOADS_BUTTON)

        expected = exists(DownloadManager.SHOW_ALL_DOWNLOADS, Settings.FIREFOX_TIMEOUT, left_top_half_region)
        assert_true(self, expected, '\'Show all downloads\' button is aligned RTL.')

        downloads_button = find(NavBar.DOWNLOADS_BUTTON)
        show_all_downloads_button = find(DownloadManager.SHOW_ALL_DOWNLOADS)

        expected = exists(DownloadFiles.DOWNLOADS_PANEL_20MB_COMPLETED_RTL, Settings.FIREFOX_TIMEOUT, left_top_half_region)
        assert_true(self, expected, 'The 20MB download is complete and aligned RTL.')

        file_20_mb = find(DownloadFiles.DOWNLOADS_PANEL_20MB_COMPLETED_RTL)
        region_20_mb = Region(file_20_mb.x, file_20_mb.y - 10,
                              file_20_mb.x, show_all_downloads_button.y - file_20_mb.y)

        expected = region_20_mb.exists(DownloadFiles.DOWNLOAD_TYPE_ICON, Settings.FIREFOX_TIMEOUT) or region_20_mb.exists(
            DownloadFiles.DOWNLOAD_TYPE_ICON_ZIP, Settings.FIREFOX_TIMEOUT)
        assert_true(self, expected, '20 MB file icon is aligned RTL.')
        region_20_mb_containing_folder = Region(downloads_button.x, file_20_mb.y,
                                                file_20_mb.x, show_all_downloads_button.y - file_20_mb.y)

        expected = region_20_mb_containing_folder.exists(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER, Settings.FIREFOX_TIMEOUT)
        assert_true(self, expected, '20 MB file Containing folder button is aligned RTL.')

        expected = exists(DownloadFiles.DOWNLOADS_PANEL_10MB_COMPLETED_RTL, Settings.FIREFOX_TIMEOUT, left_top_half_region)
        assert_true(self, expected, 'The 10MB download is complete and aligned RTL.')

        file_10_mb = find(DownloadFiles.DOWNLOADS_PANEL_10MB_COMPLETED_RTL)
        region_10_mb = Region(file_10_mb.x, file_10_mb.y - 10,
                              file_10_mb.x, file_20_mb.y - file_10_mb.y)

        expected = region_10_mb.exists(DownloadFiles.DOWNLOAD_TYPE_ICON, Settings.FIREFOX_TIMEOUT) or region_10_mb.exists(
            DownloadFiles.DOWNLOAD_TYPE_ICON_ZIP, Settings.FIREFOX_TIMEOUT)
        assert_true(self, expected, '10 MB file icon is aligned RTL.')

        region_10_mb_containing_folder = Region(downloads_button.x, file_10_mb.y,
                                                file_10_mb.x, file_20_mb.y - file_10_mb.y)

        expected = region_10_mb_containing_folder.exists(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER, Settings.FIREFOX_TIMEOUT)
        assert_true(self, expected, '10 MB file Containing folder button is aligned RTL.')

        expected = exists(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED_RTL, Settings.FIREFOX_TIMEOUT, left_top_half_region)
        assert_true(self, expected, 'The 5MB download is complete and aligned RTL.')

        file_5_mb = find(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED_RTL)
        region_5_mb_icon = Region(file_5_mb.x, file_5_mb.y - 10,
                                  file_5_mb.x, file_10_mb.y - file_5_mb.y)

        expected = region_5_mb_icon.exists(DownloadFiles.DOWNLOAD_TYPE_ICON_ZIP, Settings.FIREFOX_TIMEOUT) or region_5_mb_icon.exists(
            DownloadFiles.DOWNLOAD_TYPE_ICON, Settings.FIREFOX_TIMEOUT)
        assert_true(self, expected, '5 MB file icon is aligned RTL.')
        region_5_mb_containing_folder = Region(downloads_button.x, file_5_mb.y,
                                               file_5_mb.x, file_10_mb.y - file_5_mb.y)

        expected = region_5_mb_containing_folder.exists(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER, Settings.FIREFOX_TIMEOUT)
        assert_true(self, expected, '5 MB file Containing folder button is aligned RTL.')

    def teardown(self):
        downloads_cleanup()
