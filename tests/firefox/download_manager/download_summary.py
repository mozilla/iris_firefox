# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.download_manager import DownloadManager
from targets.firefox.firefox_ui.helpers.download_manager_utils import DownloadFiles, downloads_cleanup, download_file, \
    select_throttling, NetworkOption
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Download Summary is properly displayed.',
        locale=['en-US'],
        test_case_id='99484',
        test_suite_id='1827',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        # Wait for the page to be loaded.
        try:
            wait(DownloadFiles.VERY_LARGE_FILE_1GB, 10)
            logger.debug('File is present in the page.')
        except FindError:
            raise FindError('File is not present in the page.')

        select_throttling(NetworkOption.GOOD_3G)

        download_file(DownloadFiles.VERY_LARGE_FILE_1GB, DownloadFiles.OK)

        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert expected is True, '\'Downloads\' button found.'

        # Check download summary.
        expected = exists(DownloadFiles.DOWNLOAD_FILE_NAME_1GB, 10)
        assert expected is True, 'The 1GB download in progress is properly displayed.'

        expected = exists(DownloadManager.DownloadsPanel.TIME_LEFT.similar(0.7), 10)
        assert expected is True, 'Time left information is displayed.'

        expected = exists(DownloadManager.DownloadsPanel.BYTES_SECOND, 10)
        assert expected is True, 'Speed of download is displayed.'

        # Cancel the download.
        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL, 10)
        assert expected is True, 'The \'X\' button is found in the Downloads panel.'

        click(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL)

    def teardown(self):
        downloads_cleanup()
