# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.helpers.customize_utils import auto_hide_download_button
from targets.firefox.firefox_ui.helpers.download_manager_utils import *
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Downloading by Drag & Drop.',
        locale=['en-US'],
        test_case_id='108006',
        test_suite_id='1827',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        # Enable the download button in the nav bar.
        auto_hide_download_button()

        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert expected is True, 'Downloads button successfully activated in the nav bar.'

        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        # Wait for the page to be loaded.
        try:
            wait(DownloadFiles.VERY_LARGE_FILE_1GB, 10)
            logger.debug('File is present in the page.')
        except FindError:
            raise FindError('File is not present in the page.')

        select_throttling(NetworkOption.GPRS)

        max_attempts = 10
        while max_attempts > 0:
            if exists(DownloadFiles.VERY_LARGE_FILE_1GB, 2):
                # Wait a moment to ensure button can be grabbed for drag operation
                expected = exists(DownloadFiles.VERY_LARGE_FILE_1GB, 10)
                assert expected is True, 'Downloads button successfully activated in the nav bar.'
                drag_drop(DownloadFiles.VERY_LARGE_FILE_1GB, NavBar.DOWNLOADS_BUTTON, duration=2)
                max_attempts = 0
            max_attempts -= 1

        expected = exists(DownloadFiles.DOWNLOAD_FILE_NAME_1GB, 10)
        assert expected is True, 'The downloaded file name is properly displayed in the Downloads panel.'

        # Cancel the download.
        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL, 10)
        assert expected is True, 'The \'X\' button is found in the Downloads panel.'

        click(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL)

    def teardown(self):
        downloads_cleanup()
