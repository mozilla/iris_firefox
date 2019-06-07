# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from src.core.api.mouse import mouse
from targets.firefox.firefox_ui.download_manager import DownloadManager
from targets.firefox.firefox_ui.helpers.customize_utils import auto_hide_download_button
from targets.firefox.firefox_ui.helpers.download_manager_utils import DownloadFiles, downloads_cleanup, download_file, \
    select_throttling, NetworkOption
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Clear preview Panel when file is downloading.',
        locale=['en-US'],
        test_case_id='99822',
        test_suite_id='1827',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        download_files_list = [DownloadFiles.EXTRA_SMALL_FILE_5MB, DownloadFiles.VERY_LARGE_FILE_1GB]

        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        # Wait for the page to be loaded.
        try:
            wait(DownloadFiles.VERY_LARGE_FILE_1GB, 10)
            logger.debug('File is present in the page.')
        except FindError:
            raise FindError('File is not present in the page.')

        select_throttling(NetworkOption.GOOD_3G)

        for pattern in download_files_list:
            download_file(pattern, DownloadFiles.OK)
            file_index = download_files_list.index(pattern)

            if file_index == 0:
                expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
                assert expected is True, 'Download button found in the page.'

            click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

        # Open the Downloads Panel.
        click(NavBar.DOWNLOADS_BUTTON)

        # Check that the 5MB download is complete.
        expected = exists(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED, 90)
        assert expected is True, 'The 5MB download is complete.'

        # Open the context menu and select 'Clear Preview Panel'.
        right_click(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED)
        type(text='a')

        # Check that the 1GB download in progress is still displayed.
        expected = exists(DownloadFiles.DOWNLOAD_FILE_NAME_1GB, 10)
        assert expected is True, 'The 1GB download in progress is properly displayed.'

        # Stop the active download.
        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL, 10)
        assert expected is True, 'The \'X\' button is properly displayed.'
        click(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL)

    def teardown(self):
        downloads_cleanup()
