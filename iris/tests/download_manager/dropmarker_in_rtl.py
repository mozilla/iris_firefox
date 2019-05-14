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
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        self.set_profile_pref({'browser.download.dir': IrisCore.get_downloads_dir()})
        self.set_profile_pref({'browser.download.folderList': 2})
        self.set_profile_pref({'browser.download.useDownloadDir': True})
        return

    def run(self):
        download_files_list = [DownloadFiles.SMALL_FILE_20MB, DownloadFiles.SMALL_FILE_10MB,
                               DownloadFiles.EXTRA_SMALL_FILE_5MB]

        # Change firefox alignment to be Right-To-Left.
        change_preference('intl.uidirection', '2')

        # Check if main firefox buttons are aligned RTL.
        right_top_corner_region = Screen.UPPER_RIGHT_CORNER.top_half()

        navbar_back_button_rtl = exists(NavBar.BACK_BUTTON_RTL, Settings.FIREFOX_TIMEOUT, right_top_corner_region)
        assert_true(self, navbar_back_button_rtl, '\'Back\' button is aligned RTL.')

        navbar_home_button = exists(NavBar.HOME_BUTTON, Settings.FIREFOX_TIMEOUT, right_top_corner_region)
        assert_true(self, navbar_home_button, '\'Home\' button is aligned RTL.')

        navbar_forward_button_rtl = exists(NavBar.FORWARD_BUTTON_RTL, Settings.FIREFOX_TIMEOUT, right_top_corner_region)
        assert_true(self, navbar_forward_button_rtl, '\'Forward\' button is aligned RTL.')

        navbar_reload_button_rtl = exists(NavBar.RELOAD_BUTTON_RTL, Settings.FIREFOX_TIMEOUT, right_top_corner_region)
        assert_true(self, navbar_reload_button_rtl, '\'Reload\' button is aligned RTL.')

        left_top_half_region = Screen.LEFT_HALF.top_half()

        locationbar_star_button_unstarred = exists(LocationBar.STAR_BUTTON_UNSTARRED, Settings.FIREFOX_TIMEOUT,
                                                   left_top_half_region)
        assert_true(self, locationbar_star_button_unstarred, '\'Star dialog\' button is aligned RTL.')

        navbar_hamburger_menu = exists(NavBar.HAMBURGER_MENU, Settings.FIREFOX_TIMEOUT, left_top_half_region)
        assert_true(self, navbar_hamburger_menu, '\'Hamburger menu\' button is aligned RTL.')

        navbar_sidebar_menu_rtl = exists(NavBar.SIDEBAR_MENU_RTL, Settings.FIREFOX_TIMEOUT, left_top_half_region)
        assert_true(self, navbar_sidebar_menu_rtl, '\'Sidebar\' button is aligned RTL.')

        navbar_library_menu = exists(NavBar.LIBRARY_MENU, Settings.FIREFOX_TIMEOUT, left_top_half_region)
        assert_true(self, navbar_library_menu, '\'Library Menu dialog\' button is aligned RTL.')

        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        for local_file in download_files_list:
            download_file(local_file, DownloadFiles.OK)
            file_index = download_files_list.index(local_file)

            if file_index == 0:
                navbar_downloads_button = exists(NavBar.DOWNLOADS_BUTTON, Settings.FIREFOX_TIMEOUT)
                assert_true(self, navbar_downloads_button, 'Download button found in the page.')

            click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(50, 0))

        # Check if Downloads Panel details are aligned RTL,
        # containing folder icon aligned on the left and download type icon aligned on the right for each file.
        navbar_downloads_button_blue = exists(NavBar.DOWNLOADS_BUTTON_BLUE, Settings.SITE_LOAD_TIMEOUT,
                                              left_top_half_region)
        assert_true(self, navbar_downloads_button_blue, '\'Downloads\'button  button is aligned RTL.')

        click(NavBar.DOWNLOADS_BUTTON)

        downloadmanager_show_all_downloads = exists(DownloadManager.SHOW_ALL_DOWNLOADS, Settings.FIREFOX_TIMEOUT,
                                                    left_top_half_region)
        assert_true(self, downloadmanager_show_all_downloads, '\'Show all downloads\' button is aligned RTL.')

        downloads_button = find(NavBar.DOWNLOADS_BUTTON)
        show_all_downloads_button = find(DownloadManager.SHOW_ALL_DOWNLOADS)

        downloads_panel_20mb_completed_rtl = exists(DownloadFiles.DOWNLOADS_PANEL_20MB_COMPLETED_RTL,
                                                    Settings.FIREFOX_TIMEOUT, left_top_half_region)
        assert_true(self, downloads_panel_20mb_completed_rtl, 'The 20MB download is complete and aligned RTL.')

        file_20_mb = find(DownloadFiles.DOWNLOADS_PANEL_20MB_COMPLETED_RTL)
        region_20_mb = Region(file_20_mb.x, file_20_mb.y - 10, file_20_mb.x, show_all_downloads_button.y - file_20_mb.y)

        download_type_icon = exists(DownloadFiles.DOWNLOAD_TYPE_ICON, Settings.FIREFOX_TIMEOUT, region_20_mb) or exists(
            DownloadFiles.DOWNLOAD_TYPE_ICON_ZIP, Settings.FIREFOX_TIMEOUT, region_20_mb)
        assert_true(self, download_type_icon, '20 MB file icon is aligned RTL.')

        region_20_mb_containing_folder = Region(downloads_button.x, file_20_mb.y, file_20_mb.x,
                                                show_all_downloads_button.y - file_20_mb.y)

        open_containing_folder = exists(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER, Settings.FIREFOX_TIMEOUT,
                                        region_20_mb_containing_folder)
        assert_true(self, open_containing_folder, '20 MB file Containing folder button is aligned RTL.')

        downloads_panel_10mb_completed_rtl = exists(DownloadFiles.DOWNLOADS_PANEL_10MB_COMPLETED_RTL,
                                                    Settings.FIREFOX_TIMEOUT, left_top_half_region)
        assert_true(self, downloads_panel_10mb_completed_rtl, 'The 10MB download is complete and aligned RTL.')

        file_10_mb = find(DownloadFiles.DOWNLOADS_PANEL_10MB_COMPLETED_RTL)
        region_10_mb = Region(file_10_mb.x, file_10_mb.y - 10, file_10_mb.x, file_20_mb.y - file_10_mb.y)

        download_type_icon = exists(DownloadFiles.DOWNLOAD_TYPE_ICON, Settings.FIREFOX_TIMEOUT, region_10_mb) or exists(
            DownloadFiles.DOWNLOAD_TYPE_ICON_ZIP, Settings.FIREFOX_TIMEOUT, region_10_mb)
        assert_true(self, download_type_icon, '10 MB file icon is aligned RTL.')

        region_10_mb_containing_folder = Region(downloads_button.x, file_10_mb.y, file_10_mb.x,
                                                file_20_mb.y - file_10_mb.y)

        open_containing_folder = exists(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER, Settings.FIREFOX_TIMEOUT,
                                        region_10_mb_containing_folder)
        assert_true(self, open_containing_folder, '10 MB file Containing folder button is aligned RTL.')

        downloads_panel_5mb_completed_rtl = exists(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED_RTL,
                                                   Settings.FIREFOX_TIMEOUT, left_top_half_region)
        assert_true(self, downloads_panel_5mb_completed_rtl, 'The 5MB download is complete and aligned RTL.')

        file_5_mb = find(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED_RTL)
        region_5_mb_icon = Region(file_5_mb.x, file_5_mb.y - 10, file_5_mb.x, file_10_mb.y - file_5_mb.y)

        download_type_icon_zip = exists(DownloadFiles.DOWNLOAD_TYPE_ICON_ZIP, Settings.FIREFOX_TIMEOUT,
                                        region_5_mb_icon) or exists(
            DownloadFiles.DOWNLOAD_TYPE_ICON, Settings.FIREFOX_TIMEOUT, region_5_mb_icon)
        assert_true(self, download_type_icon_zip, '5 MB file icon is aligned RTL.')

        region_5_mb_containing_folder = Region(downloads_button.x, file_5_mb.y, file_5_mb.x, file_10_mb.y - file_5_mb.y)

        open_containing_folder = exists(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER, Settings.FIREFOX_TIMEOUT,
                                        region_5_mb_containing_folder)
        assert_true(self, open_containing_folder, '5 MB file Containing folder button is aligned RTL.')

    def teardown(self):
        downloads_cleanup()
