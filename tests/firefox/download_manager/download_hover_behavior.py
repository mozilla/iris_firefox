# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.download_manager import DownloadManager
from targets.firefox.firefox_ui.helpers.download_manager_utils import *
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Hover behavior.',
        locale=['en-US'],
        test_case_id='99478',
        test_suite_id='1827',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        download_file(DownloadFiles.VERY_LARGE_FILE_1GB, DownloadFiles.OK)

        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert expected is True, 'Downloads button found.'

        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL, 10)
        assert expected is True, 'The \'X\' button is properly displayed.'

        # Hover the 'X' button.
        hover(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL)
        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL_HIGHLIGHTED, 10)
        assert expected is True, 'The \'X\' button is highlighted properly.'

        # Click the 'X' button.
        click(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL_HIGHLIGHTED)
        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_RETRY_HIGHLIGHTED, 10)
        assert expected is True, 'The Retry button is highlighted properly.'

        expected = exists(DownloadFiles.DOWNLOAD_FILE_NAME_1GB, 10)
        assert expected is True, 'The downloaded file name is properly displayed.'

        # Hover the file name.
        hover(DownloadFiles.DOWNLOAD_FILE_NAME_1GB)
        expected = exists(DownloadFiles.DOWNLOAD_CANCELED, 10)
        assert expected is True, 'The status and the source page are properly displayed when hovering the downloaded'
        ' file name.'

    def teardown(self):
        downloads_cleanup()
