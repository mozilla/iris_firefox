# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.download_manager import DownloadManager
from targets.firefox.firefox_ui.helpers.download_manager_utils import *
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Show all downloads states' with no download items.",
        locale=["en-US"],
        test_case_id="99503",
        test_suite_id="1827",
        profile=Profiles.BRAND_NEW,
        preferences={
            "browser.download.dir": PathManager.get_downloads_dir(),
            "browser.download.folderList": 2,
            "browser.download.useDownloadDir": True,
            "browser.warnOnQuit": False,
        },
    )
    def run(self, firefox):
        download_files_list = [
            DownloadFiles.EXTRA_LARGE_FILE_512MB,
            DownloadFiles.MEDIUM_FILE_100MB,
            DownloadFiles.VERY_LARGE_FILE_1GB,
        ]

        navigate(LocalWeb.DOWNLOAD_TEST_SITE)

        # Wait for the page to be loaded.
        try:
            wait(DownloadFiles.VERY_LARGE_FILE_1GB, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug("File is present in the page.")
        except FindError:
            raise FindError("File is not present in the page.")

        select_throttling(NetworkOption.GOOD_3G)

        expected = exists(NavBar.RELOAD_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected is True, "Reload button found in the page."
        click(NavBar.RELOAD_BUTTON)

        expected = exists(DownloadFiles.STATUS_200, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected is True, "Page successfully reloaded."

        for f in download_files_list:

            download_file(f, DownloadFiles.OK)
            file_index = download_files_list.index(f)

            if file_index == 0:
                time.sleep(Settings.DEFAULT_SYSTEM_DELAY)
            else:
                click(NavBar.DOWNLOADS_BUTTON)

            expected = exists(DownloadManager.DownloadState.PROGRESS, FirefoxSettings.FIREFOX_TIMEOUT)
            assert expected is True, "Progress information is displayed."
            expected = exists(DownloadManager.DownloadState.SPEED_PER_SECOND, FirefoxSettings.FIREFOX_TIMEOUT)
            assert expected is True, "Speed information is displayed."

        # Close download panel.
        click(NavBar.DOWNLOADS_BUTTON.target_offset(-50, 0))

        # Cancel all in progress downloads.
        for step in cancel_in_progress_downloads_from_the_library():
            assert expected is True, (step.resolution, step.message)

        # Remove download from history
        time.sleep(Settings.DEFAULT_UI_DELAY)
        click(NavBar.DOWNLOADS_BUTTON)
        download_history_opened = exists(DownloadManager.SHOW_ALL_DOWNLOADS)
        assert download_history_opened, "Download progress window is still closed "

        expected = Screen.UPPER_RIGHT_CORNER.exists(
            DownloadManager.DownloadState.CANCELLED.similar(0.7), 10
        ) or Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.COMPLETED.similar(0.7),
                                              FirefoxSettings.FIREFOX_TIMEOUT)
        remove_file_pattern = (
            DownloadManager.DownloadState.CANCELLED
            if Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.CANCELLED.similar(0.7),
                                                FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
            else DownloadManager.DownloadState.COMPLETED
        )

        while expected:
            right_click(remove_file_pattern)
            assert expected is True, "Remove downloaded item."
            click(DownloadManager.DownloadsContextMenu.REMOVE_FROM_HISTORY)
            time.sleep(Settings.DEFAULT_UI_DELAY)

            if Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.CANCELLED.similar(0.7),
                                                FirefoxSettings.SHORT_FIREFOX_TIMEOUT):
                expected = True
                remove_file_pattern = DownloadManager.DownloadState.CANCELLED
            elif Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.COMPLETED.similar(0.7),
                                                  FirefoxSettings.SHORT_FIREFOX_TIMEOUT):
                expected = True
                remove_file_pattern = DownloadManager.DownloadState.COMPLETED
            elif Screen.UPPER_RIGHT_CORNER.exists(DownloadManager.DownloadState.FAILED.similar(0.7),
                                                  FirefoxSettings.SHORT_FIREFOX_TIMEOUT):
                expected = True
                remove_file_pattern = DownloadManager.DownloadState.FAILED
            else:
                expected = False

        # Check that the Downloads Library window is displayed.
        for step in open_show_all_downloads_window_from_library_menu():
            expected = exists(Library.TITLE, FirefoxSettings.FIREFOX_TIMEOUT)
            assert expected is True, "Library window is displayed."
            assert expected is True, (step.resolution, step.message)

        expected = \
            exists(DownloadFiles.DOWNLOAD_TYPE_ICON.similar(0.95), FirefoxSettings.TINY_FIREFOX_TIMEOUT) \
            or \
            exists(DownloadFiles.DOWNLOAD_TYPE_ICON_ZIP.similar(0.95), FirefoxSettings.TINY_FIREFOX_TIMEOUT
                   )
        assert expected is False, "There are no downloads displayed in Library, Downloads section."

        click_window_control("close")

    def teardown(self):
        downloads_cleanup()
