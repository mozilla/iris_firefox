# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.download_manager import DownloadManager
from targets.firefox.firefox_ui.helpers.download_manager_utils import DownloadFiles, downloads_cleanup, download_file
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Download links can be copied via drag & drop/context menu.',
        locale=['en-US'],
        test_case_id='99490',
        test_suite_id='1827',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        # Perform some downloads.
        download_files_list = [DownloadFiles.SMALL_FILE_20MB, DownloadFiles.SMALL_FILE_10MB,
                               DownloadFiles.EXTRA_SMALL_FILE_5MB]

        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        for pattern in download_files_list:
            download_file(pattern, DownloadFiles.OK)
            file_index = download_files_list.index(pattern)

            if file_index == 0:
                expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
                assert expected is True, 'Download button found in the page.'

            click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

        # Open the Downloads Panel.
        expected = exists(NavBar.DOWNLOADS_BUTTON_BLUE, 30)
        assert expected is True, '\'Downloads\' button found.'
        click(NavBar.DOWNLOADS_BUTTON_BLUE)

        # Check that the 5MB download is complete.
        expected = exists(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED, 10)
        assert expected is True, 'The 5MB download is complete.'

        expected = exists(DownloadFiles.DOWNLOAD_FILE_NAME_10MB, 10)
        assert expected is True, 'The 10MB file found in the download manager.'

        # Drag and drop the 10MB file from download manager in to the tab bar.
        drag_drop(DownloadFiles.DOWNLOAD_FILE_NAME_10MB, Location(400, 30))

        try:
            wait(DownloadFiles.OK, 5)
            logger.debug('The download dialog is triggered in the page.')
            click_window_control('close')
            time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        except FindError:
            raise FindError('The download dialog is not triggered in the page.')

        # Right click on another download and select 'Copy Download Link'.
        click(NavBar.DOWNLOADS_BUTTON)
        expected = exists(DownloadFiles.DOWNLOAD_FILE_NAME_20MB, 10)
        assert expected is True, 'The 20MB file found in the download manager.'

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
            time.sleep(Settings.DEFAULT_UI_DELAY)
        except FindError:
            raise FindError('The download dialog is not triggered in the page.')

    def teardown(self):
        downloads_cleanup()
