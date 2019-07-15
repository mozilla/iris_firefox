# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.helpers.customize_utils import *
from targets.firefox.firefox_ui.helpers.download_manager_utils import *
from targets.firefox.firefox_ui.more_tools import MoreTools
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The downloads button works properly positioned in the Overflow Menu.',
        locale=['en-US'],
        test_case_id='245607',
        test_suite_id='1827',
        blocked_by={'id': '1527607', 'platform': OSPlatform.ALL},
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        download_files_list = [DownloadFiles.SMALL_FILE_20MB, DownloadFiles.SMALL_FILE_10MB,
                               DownloadFiles.EXTRA_SMALL_FILE_5MB]
        downloads_library_list = [DownloadFiles.LIBRARY_DOWNLOADS_20MB, DownloadFiles.LIBRARY_DOWNLOADS_10MB,
                                  DownloadFiles.LIBRARY_DOWNLOADS_5MB_HIGHLIGHTED]

        click_hamburger_menu_option('Customize...')

        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert expected is True, 'Download button is available.'

        expected = exists(CustomizePage.OVERFLOW_MENU_ICON, 10)
        assert expected is True, 'Overflow menu drop area is displayed.'

        drag_drop(NavBar.DOWNLOADS_BUTTON, CustomizePage.OVERFLOW_MENU_ICON, duration=0.5)

        expected = exists(Library.DOWNLOADS, 10)
        assert expected is True, 'Download option is placed in Overflow menu.'

        close_customize_page()

        expected = exists(NavBar.MORE_TOOLS, 10)
        assert expected is True, 'More tools button is available in NavBar.'

        click(NavBar.MORE_TOOLS)

        expected = exists(MoreTools.DOWNLOADS, 10)
        assert expected is True, 'Download option is placed in Overflow menu.'

        click(MoreTools.DOWNLOADS.target_offset(-50, 0))

        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        for pattern in download_files_list:
            download_file(pattern, DownloadFiles.OK)

        expected = exists(NavBar.MORE_TOOLS, 10)
        assert expected is True, 'More tools button is available in NavBar.'

        click(NavBar.MORE_TOOLS)

        download_option = find(MoreTools.DOWNLOADS_OPTION)
        region_download_button_blue = Region(download_option.x - 50, download_option.y - 20, 100, 100)
        expected = region_download_button_blue.exists(NavBar.DOWNLOADS_BUTTON_BLUE.similar(0.99), 30)
        assert expected is True, 'Download button turns blue in the overflow menu when download is completed.'

        open_downloads()

        if OSHelper.is_linux():
            drag_drop(Library.TITLE, DownloadFiles.ABOUT, duration=2)

        # Check that all downloads are displayed in Downloads category.
        for pattern in downloads_library_list:
            expected = exists(pattern, 50)
            assert expected is True, '%s file found in the Library, Downloads section.' % str(pattern.get_filename())

        click_window_control('close')
        close_window()


def teardown(self):
    downloads_cleanup()
