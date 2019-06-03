# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.helpers.download_manager_utils import *
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Notifications are displayed if downloads are finished or new ones initiated.',
        locale=['en-US'],
        test_case_id='99493',
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

        if OSHelper.is_linux():
            download_file(DownloadFiles.EXTRA_SMALL_FILE_5MB, DownloadFiles.OK)
        else:
            download_file(DownloadFiles.EXTRA_SMALL_FILE_5MB, DownloadFiles.OK)

        expected = exists(DownloadManager.DownloadState.PROGRESS, 10)
        assert expected is True, 'Progress information is displayed.'
        expected = exists(DownloadManager.DownloadState.SPEED_PER_SECOND, 10)
        assert expected is True, 'Speed information is displayed.'

        # Download a second file to check the blue download arrow
        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert expected is True, 'Download button found in the page.'

        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))
        download_file(DownloadFiles.EXTRA_SMALL_FILE_5MB, DownloadFiles.OK)
        expected = exists(NavBar.DOWNLOADS_BUTTON_BLUE, 90)
        assert expected is True, 'Downloads button found.'

        # Cancel all 'in progress' downloads.
        cancel_and_clear_downloads()
        # Refocus the firefox window.
        exists(LocationBar.STAR_BUTTON_UNSTARRED, 10)
        click(LocationBar.STAR_BUTTON_UNSTARRED.target_offset(+30, 0))

    def teardown(self):
        downloads_cleanup()
