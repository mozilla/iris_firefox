# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.download_manager import DownloadManager
from targets.firefox.firefox_ui.helpers.download_manager_utils import *
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Show all downloads states\' with no download items.',
        locale=['en-US'],
        test_case_id='99503',
        test_suite_id='1827',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        download_files_list = [DownloadFiles.EXTRA_LARGE_FILE_512MB,
                               DownloadFiles.MEDIUM_FILE_100MB, DownloadFiles.VERY_LARGE_FILE_1GB]

        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        # Wait for the page to be loaded.
        try:
            wait(DownloadFiles.VERY_LARGE_FILE_1GB, 10)
            logger.debug('File is present in the page.')
        except FindError:
            raise FindError('File is not present in the page.')

        select_throttling(NetworkOption.GOOD_3G)

        expected = exists(NavBar.RELOAD_BUTTON, 10)
        assert expected is True, 'Reload button found in the page.'
        click(NavBar.RELOAD_BUTTON)

        expected = exists(DownloadFiles.STATUS_200, 10)
        assert expected is True, 'Page successfully reloaded.'

        for f in download_files_list:

            download_file(f, DownloadFiles.OK)
            file_index = download_files_list.index(f)

            if file_index == 0:
                time.sleep(Settings.DEFAULT_SYSTEM_DELAY)
            else:
                click(NavBar.DOWNLOADS_BUTTON)

            expected = exists(DownloadManager.DownloadState.PROGRESS, 10)
            assert expected is True, 'Progress information is displayed.'
            expected = exists(DownloadManager.DownloadState.SPEED_PER_SECOND, 10)
            assert expected is True, 'Speed information is displayed.'

        # Close download panel.
        click(NavBar.DOWNLOADS_BUTTON.target_offset(-50, 0))

        # Cancel all in progress downloads.
        for step in cancel_in_progress_downloads_from_the_library():
            assert expected is True, (step.resolution, step.message)

        #
        click(NavBar.DOWNLOADS_BUTTON)
        expected = Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.CANCELED.similar(0.9), 10) or \
                   Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.COMPLETED.similar(0.9), 10)
        remove_file_pattern = DownloadManager.DownloadState.CANCELED if \
            Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.CANCELED.similar(0.9), 5) else \
            DownloadManager.DownloadState.COMPLETED

        while expected:
            right_click(remove_file_pattern)
            assert expected is True, 'Remove downloaded item.'
            click(DownloadManager.DownloadsContextMenu.REMOVE_FROM_HISTORY)
            time.sleep(Settings.DEFAULT_UI_DELAY)

            if Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.CANCELED.similar(0.9), 5):
                expected = True
                remove_file_pattern = DownloadManager.DownloadState.CANCELED
            elif Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.COMPLETED.similar(0.9), 5):
                expected = True
                remove_file_pattern = DownloadManager.DownloadState.COMPLETED
            elif Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.FAILED.similar(0.9), 5):
                expected = True
                remove_file_pattern = DownloadManager.DownloadState.FAILED
            else:
                expected = False

        # Check that the Downloads Library window is displayed.
        for step in open_show_all_downloads_window_from_library_menu():
            expected = exists(Library.TITLE, 10)
            assert expected is True, 'Library window is displayed.'
            assert expected is True, (step.resolution, step.message)

        expected = exists(DownloadFiles.DOWNLOAD_TYPE_ICON.similar(0.95), 5) or exists(
            DownloadFiles.DOWNLOAD_TYPE_ICON_ZIP.similar(0.95), 5)
        assert expected is False, 'There are no downloads displayed in Library, Downloads section.'

        click_window_control('close')

    def teardown(self):
        downloads_cleanup()
