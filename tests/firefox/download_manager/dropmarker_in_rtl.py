# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.about_config import AboutConfig
from targets.firefox.firefox_ui.helpers.customize_utils import auto_hide_download_button
from targets.firefox.firefox_ui.helpers.download_manager_utils import *
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Dropmarker in RTL.',
        locale=['en-US'],
        test_case_id='99500',
        test_suite_id='1827',
        blocked_by={'id': '1554158', 'platform': OSPlatform.ALL},
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        region = Region(0, 0, Screen.SCREEN_WIDTH, 2 * Screen.SCREEN_HEIGHT / 3)

        # Change firefox alignment to be Right-To-Left.
        navigate('about:config')
        click(AboutConfig.ACCEPT_RISK.similar(0.7))

        expected = region.exists(AboutConfig.DEFAULT_STATUS_PATTERN, 10)
        assert expected is True, 'The \'about:config\' page successfully loaded and default status is correct.'

        paste('intl.uidirection')
        type(Key.ENTER)

        expected = exists(AboutConfig.PreferenceName.INTL_UIDIRECTION, 10)
        assert expected is True, 'The \'intl.uidirection\' preference is displayed.'

        double_click(AboutConfig.PreferenceName.INTL_UIDIRECTION)
        expected = exists(AboutConfig.ENTER_INTEGER_VALUE, 10)
        assert expected is True, 'Integer value window is open.'

        type('2')
        expected = exists(DownloadFiles.OK, 10)
        assert expected is True, '\'OK\' button is available.'
        click(DownloadFiles.OK)

        expected = exists(AboutConfig.MODIFIED_STATUS_PATTERN, 10)
        assert expected is True, \
            'The \'intl.uidirection\' preference has status \'modified\' after the preference has changed.'

        # Check if main firefox buttons are aligned RTL.
        region_right = Screen.UPPER_RIGHT_CORNER.top_half()
        expected = region_right.exists(NavBar.BACK_BUTTON_RTL, 10)
        assert expected is True, '\'Back\' button is aligned RTL.'
        expected = region_right.exists(NavBar.HOME_BUTTON, 10)
        assert expected is True, '\'Home\' button is aligned RTL.'
        expected = region_right.exists(NavBar.FORWARD_BUTTON_RTL, 10)
        assert expected is True, '\'Forward\' button is aligned RTL.'
        expected = region_right.exists(NavBar.RELOAD_BUTTON_RTL, 10)
        assert expected is True, '\'Reload\' button is aligned RTL.'
        region_left = Screen.LEFT_HALF.top_half()
        expected = region_left.exists(LocationBar.STAR_BUTTON_UNSTARRED)
        assert expected is True, '\'Star dialog\' button is aligned RTL.'
        expected = region_left.exists(NavBar.HAMBURGER_MENU)
        assert expected is True, '\'Hamburger menu\' button is aligned RTL.'
        expected = region_left.exists(NavBar.SIDEBAR_MENU_RTL)
        assert expected is True, '\'Sidebar\' button is aligned RTL.'
        expected = region_left.exists(NavBar.LIBRARY_MENU)
        assert expected is True, '\'Library Menu dialog\' button is aligned RTL.'

        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)
        download_files_list = [DownloadFiles.SMALL_FILE_20MB, DownloadFiles.SMALL_FILE_10MB,
                               DownloadFiles.EXTRA_SMALL_FILE_5MB]

        for f in download_files_list:
            download_file(f, DownloadFiles.OK)
            file_index = download_files_list.index(f)

            if file_index == 0:
                expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
                assert expected is True, 'Download button found in the page.'

            click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(50, 0))

        # Check if Downloads Panel details are aligned RTL,
        # containing folder icon aligned on the left and download type icon aligned on the right for each file.
        expected = region_left.exists(NavBar.DOWNLOADS_BUTTON_BLUE, 50)
        assert expected is True, '\'Downloads\'button  button is aligned RTL.'

        click(NavBar.DOWNLOADS_BUTTON)

        expected = region_left.exists(DownloadManager.SHOW_ALL_DOWNLOADS, 10)
        assert expected is True, '\'Show all downloads\' button is aligned RTL.'

        downloads_button = find(NavBar.DOWNLOADS_BUTTON)
        show_all_downloads_button = find(DownloadManager.SHOW_ALL_DOWNLOADS)

        expected = region_left.exists(DownloadFiles.DOWNLOADS_PANEL_20MB_COMPLETED_RTL, 10)
        assert expected is True, 'The 20MB download is complete and aligned RTL.'

        file_20_mb = find(DownloadFiles.DOWNLOADS_PANEL_20MB_COMPLETED_RTL)
        region_20_mb = Region(file_20_mb.x, file_20_mb.y - 10,
                              file_20_mb.x, show_all_downloads_button.y - file_20_mb.y)

        expected = region_20_mb.exists(DownloadFiles.DOWNLOAD_TYPE_ICON, 10) or region_20_mb.exists(
            DownloadFiles.DOWNLOAD_TYPE_ICON_ZIP, 10)
        assert expected is True, '20 MB file icon is aligned RTL.'
        region_20_mb_containing_folder = Region(downloads_button.x, file_20_mb.y,
                                                file_20_mb.x, show_all_downloads_button.y - file_20_mb.y)

        expected = region_20_mb_containing_folder.exists(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER, 10)
        assert expected is True, '20 MB file Containing folder button is aligned RTL.'

        expected = region_left.exists(DownloadFiles.DOWNLOADS_PANEL_10MB_COMPLETED_RTL, 10)
        assert expected is True, 'The 10MB download is complete and aligned RTL.'

        file_10_mb = find(DownloadFiles.DOWNLOADS_PANEL_10MB_COMPLETED_RTL)
        region_10_mb = Region(file_10_mb.x, file_10_mb.y - 10,
                              file_10_mb.x, file_20_mb.y - file_10_mb.y)

        expected = region_10_mb.exists(DownloadFiles.DOWNLOAD_TYPE_ICON, 10) or region_10_mb.exists(
            DownloadFiles.DOWNLOAD_TYPE_ICON_ZIP, 10)
        assert expected is True, '10 MB file icon is aligned RTL.'

        region_10_mb_containing_folder = Region(downloads_button.x, file_10_mb.y,
                                                file_10_mb.x, file_20_mb.y - file_10_mb.y)

        expected = region_10_mb_containing_folder.exists(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER, 10)
        assert expected is True, '10 MB file Containing folder button is aligned RTL.'

        expected = region_left.exists(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED_RTL, 10)
        assert expected is True, 'The 5MB download is complete and aligned RTL.'

        file_5_mb = find(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED_RTL)
        region_5_mb_icon = Region(file_5_mb.x, file_5_mb.y - 10,
                                  file_5_mb.x, file_10_mb.y - file_5_mb.y)

        expected = region_5_mb_icon.exists(DownloadFiles.DOWNLOAD_TYPE_ICON_ZIP, 10) or region_5_mb_icon.exists(
            DownloadFiles.DOWNLOAD_TYPE_ICON, 10)
        assert expected is True, '5 MB file icon is aligned RTL.'
        region_5_mb_containing_folder = Region(downloads_button.x, file_5_mb.y,
                                               file_5_mb.x, file_10_mb.y - file_5_mb.y)

        expected = region_5_mb_containing_folder.exists(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER, 10)
        assert expected is True, '5 MB file Containing folder button is aligned RTL.'

    def teardown(self):
        downloads_cleanup()
