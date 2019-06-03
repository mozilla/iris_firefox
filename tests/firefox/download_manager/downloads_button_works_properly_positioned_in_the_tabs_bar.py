# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.helpers.download_manager_utils import *
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The downloads button works properly positioned in the tabs bar.',
        locale=['en-US'],
        test_case_id='99473',
        test_suite_id='1827',
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

        drag_drop(NavBar.DOWNLOADS_BUTTON, NavBar.BAR, duration=0.5)

        close_customize_page()

        expected = exists(NavBar.CUSTOM_DOWNLOADS_BUTTON, 10)
        assert expected is True, 'Custom Download button is available in tabs bar.'

        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        for pattern in download_files_list:
            download_file(pattern, DownloadFiles.OK)

        expected = exists(NavBar.CUSTOM_DOWNLOADS_BUTTON_BLUE, 30)
        assert expected is True, 'Download button turns blue when download is completed.'

        open_downloads()

        if OSHelper.is_linux():
            drag_drop(Library.TITLE, DownloadFiles.EXTRA_SMALL_FILE_5MB, duration=2)

        expected = exists(NavBar.CUSTOM_DOWNLOADS_BUTTON, 10)
        assert expected is True, 'Download button turns back to default color.'

        # Check that all downloads are displayed in Downloads category.
        for pattern in downloads_library_list:
            expected = exists(pattern, 50)
            assert expected is True, '%s file found in the Library, Downloads section.' % str(pattern.get_filename())

        click_window_control('close')

        # Cancel all 'in progress' downloads.
        cancel_in_progress_downloads_from_the_library()
        # Refocus the firefox window.
        exists(LocationBar.STAR_BUTTON_UNSTARRED, 10)
        click(LocationBar.STAR_BUTTON_UNSTARRED.target_offset(+30, 0))

    def teardown(self):
        downloads_cleanup()
