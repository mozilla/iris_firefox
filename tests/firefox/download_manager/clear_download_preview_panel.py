# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from src.core.api.mouse import mouse
from targets.firefox.firefox_ui.download_manager import DownloadManager
from targets.firefox.firefox_ui.helpers.customize_utils import auto_hide_download_button
from targets.firefox.firefox_ui.helpers.download_manager_utils import *
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Clear Download History.',
        locale=['en-US'],
        test_case_id='99482',
        test_suite_id='1827',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        file_to_download = DownloadFiles.EXTRA_SMALL_FILE_5MB

        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        download_file(file_to_download, DownloadFiles.OK)

        expected = exists(NavBar.DOWNLOADS_BUTTON_BLUE, 10)
        assert expected is True, 'Downloads button found.'

        expected = exists(DownloadManager.DownloadState.COMPLETED, 10)
        assert expected is True, 'Completed information is displayed.'

        right_click(DownloadManager.DownloadState.COMPLETED)
        click(DownloadManager.DownloadsContextMenu.CLEAR_PREVIEW_PANEL)

        # Enable the download button in the nav bar.
        auto_hide_download_button()
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        # Check that all of the downloads were cleared.
        expected = exists(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON, 10)
        assert expected is True, 'Downloads button has been found.'
        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON)
        expected = exists(DownloadManager.DownloadsPanel.NO_DOWNLOADS_FOR_THIS_SESSION, 10)
        assert expected is True, 'All downloads were cleared.'

    def teardown(self):
        downloads_cleanup()
