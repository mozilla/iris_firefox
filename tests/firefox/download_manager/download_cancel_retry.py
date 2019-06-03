# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from src.core.api.mouse import mouse
from targets.firefox.firefox_ui.download_manager import DownloadManager
from targets.firefox.firefox_ui.helpers.download_manager_utils import *
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The download can be cancelled or retried.',
        locale=['en-US'],
        test_case_id='99470',
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

        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL, 10)
        assert expected is True, 'Cancel button is displayed.'

        click(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL)
        if OSHelper.get_os() != OSPlatform.LINUX:
            expected = exists(DownloadManager.DownloadState.RETRY_DOWNLOAD, 10)
            assert expected is True, 'Retry download message is displayed.'

        mouse.move(Location(Screen.SCREEN_WIDTH / 4 + 100, Screen.SCREEN_HEIGHT / 4))
        expected = exists(DownloadManager.DownloadState.CANCELED, 10)
        assert expected is True, 'Download was cancelled.'

        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_RETRY, 10)
        assert expected is True, 'Retry button is displayed.'

        click(DownloadManager.DownloadsPanel.DOWNLOAD_RETRY)
        mouse.move(Location(Screen.SCREEN_WIDTH / 4 + 100, Screen.SCREEN_HEIGHT / 4))
        expected = exists(DownloadManager.DownloadState.PROGRESS, 10)
        assert expected is True, 'Download was restarted.'

        # Cancel 'in progress' download.
        click(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL)

    def teardown(self):
        downloads_cleanup()
