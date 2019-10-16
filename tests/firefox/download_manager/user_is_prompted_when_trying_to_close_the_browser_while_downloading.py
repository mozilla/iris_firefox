# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.download_manager import DownloadManager
from targets.firefox.firefox_ui.helpers.download_manager_utils import (
    DownloadFiles,
    downloads_cleanup,
    download_file,
    select_throttling,
    NetworkOption,
    cancel_and_clear_downloads,
)
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="The user is prompted when trying to close the browser while downloading files.",
        locale=["en-US"],
        test_case_id="99492",
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
            DownloadFiles.VERY_LARGE_FILE_1GB,
            DownloadFiles.EXTRA_LARGE_FILE_512MB,
        ]

        navigate(LocalWeb.DOWNLOAD_TEST_SITE)

        # Wait for the page to be loaded.
        try:
            wait(DownloadFiles.VERY_LARGE_FILE_1GB, 30)
            logger.debug("File is present in the page.")
        except FindError:
            raise FindError("File is not present in the page.")

        select_throttling(NetworkOption.GOOD_3G)

        expected = exists(NavBar.RELOAD_BUTTON, 10)
        assert expected is True, "Reload button found in the page."
        click(NavBar.RELOAD_BUTTON)

        expected = exists(DownloadFiles.STATUS_200, 10)
        assert expected is True, "Page successfully reloaded."

        for pattern in download_files_list:
            download_file(pattern, DownloadFiles.OK)
            file_index = download_files_list.index(pattern)

            if file_index == 0:
                expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
                assert expected is True, "Download button found in the page."

            click(NavBar.DOWNLOADS_BUTTON.target_offset(-50, 0))

        click(NavBar.DOWNLOADS_BUTTON)
        expected = exists(DownloadManager.DownloadState.SPEED_PER_SECOND, 10)
        assert expected is True, "At least one download is in progress."

        click(NavBar.DOWNLOADS_BUTTON.target_offset(-50, 0))

        quit_firefox()

        expected = exists(DownloadFiles.CANCEL_ALL_DOWNLOADS_POP_UP, 10)
        assert expected is True, "'Cancel all downloads?' warming pop-up is displayed."

        # Dismiss warming pop-up.
        type(text=Key.ESC)

        # Cancel all 'in progress' downloads.
        cancel_and_clear_downloads()
        # Refocus the firefox window.
        exists(LocationBar.STAR_BUTTON_UNSTARRED, 10)
        click(LocationBar.STAR_BUTTON_UNSTARRED.target_offset(+30, 0))

    def teardown(self):
        downloads_cleanup()
