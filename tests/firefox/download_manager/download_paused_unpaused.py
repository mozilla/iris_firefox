# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.download_manager import DownloadManager
from targets.firefox.firefox_ui.helpers.download_manager_utils import DownloadFiles, downloads_cleanup, download_file, \
    cancel_and_clear_downloads
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The download can be paused/unpaused.',
        locale=['en-US'],
        test_case_id='99471',
        test_suite_id='1827',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        file_to_download = DownloadFiles.VERY_LARGE_FILE_1GB
        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        download_file(file_to_download, DownloadFiles.OK)

        expected = exists(DownloadManager.DownloadState.PROGRESS, 10)
        assert expected is True, 'Progress information is displayed.'

        right_click(DownloadManager.DownloadState.PROGRESS)
        click(DownloadManager.DownloadsContextMenu.PAUSE)

        expected = exists(DownloadManager.DownloadState.PAUSED, 10)
        assert expected is True, 'Download was paused.'

        right_click(DownloadManager.DownloadState.PAUSED)
        click(DownloadManager.DownloadsContextMenu.RESUME)

        expected = exists(DownloadManager.DownloadState.PROGRESS, 10)
        assert expected is True, 'Download was resumed.'

        # Cancel 'in progress' download.
        click(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL)

        # Refocus the firefox window.
        exists(LocationBar.STAR_BUTTON_UNSTARRED, 10)
        click(LocationBar.STAR_BUTTON_UNSTARRED.target_offset(+30, 0))

    def teardown(self):
        downloads_cleanup()
