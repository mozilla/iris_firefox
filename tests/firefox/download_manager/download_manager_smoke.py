# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.download_manager import DownloadManager
from targets.firefox.firefox_ui.helpers.download_manager_utils import DownloadFiles, downloads_cleanup, download_file
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Download Manager Smoke.',
        locale=['en-US'],
        test_case_id='99157',
        test_suite_id='1827',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        navigate('https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-central/')

        download_file(DownloadFiles.FIREFOX_INSTALLER.similar(0.8), DownloadFiles.OK)

        expected = exists(NavBar.DOWNLOADS_BUTTON_BLUE.similar(0.8), FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert expected is True, 'Downloads button found.'

        expected = exists(DownloadManager.DownloadState.COMPLETED, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT * 2)
        assert expected is True, 'Firefox installer download is completed.'

        expected = exists(DownloadManager.DownloadsPanel.OPEN_DOWNLOAD_FOLDER, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected is True, 'Containing folder button is available.'

        # Navigate to Downloads folder.
        click(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER)

        if OSHelper.is_linux():
            click(Pattern('linux_folder_icon.png'))

        expected = exists(DownloadManager.DOWNLOADS_FOLDER, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected is True, 'Downloads folder is displayed.'

        if OSHelper.is_mac():
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
            type('2', modifier=KeyModifier.CMD)

        expected = exists(DownloadFiles.FIREFOX_INSTALLER_HIGHLIGHTED, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected is True, 'Firefox installer is displayed in downloads folder.'

        click_window_control('close')

        expected = exists(NavBar.DOWNLOADS_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected is True, 'Download button found in the page.'

        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

    def teardown(self):
        downloads_cleanup()
