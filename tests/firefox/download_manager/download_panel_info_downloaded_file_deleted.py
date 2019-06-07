# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.download_manager import DownloadManager
from targets.firefox.firefox_ui.helpers.download_manager_utils import DownloadFiles, downloads_cleanup, download_file, \
    cancel_and_clear_downloads
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Download panel informs the user if a former download has been deleted.',
        locale=['en-US'],
        test_case_id='99481',
        test_suite_id='1827',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        download_file(DownloadFiles.EXTRA_SMALL_FILE_5MB, DownloadFiles.OK)

        expected = exists(NavBar.DOWNLOADS_BUTTON_BLUE, 10)
        assert expected is True, 'Downloads button found.'

        expected = exists(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED, 10)
        assert expected is True, 'Small size file download is completed.'

        expected = exists(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER, 10)
        assert expected is True, 'Containing folder button is available.'

        # Navigate to Downloads folder.
        click(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER)

        expected = exists(DownloadManager.DOWNLOADS_FOLDER, 10)
        assert expected is True, 'Downloads folder is displayed.'

        expected = exists(DownloadFiles.FOLDER_VIEW_5MB_HIGHLIGHTED, 10)
        assert expected is True, 'Downloaded file is found.'

        delete_selected_file()

        try:
            expected = wait_vanish(DownloadFiles.FOLDER_VIEW_5MB_HIGHLIGHTED, 10)
            assert expected is True, 'The file was successfully deleted.'
        except FindError:
            raise FindError('The file was not deleted.')

        # Close download folder window.
        click_window_control('close')

        try:
            expected = wait_vanish(DownloadManager.DOWNLOADS_FOLDER, 10)
            assert expected is True, 'The downloads folder was closed.'
        except FindError:
            raise FindError('The downloads folder was not closed.')

        # Switch the focus on firefox browser.
        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert expected is True, 'Download button found in the page.'

        click(NavBar.DOWNLOADS_BUTTON.target_offset(-70, 15))

        click(NavBar.DOWNLOADS_BUTTON)

        expected = exists(DownloadManager.Downloads.EXTRA_SMALL_FILE_5MB_ZIP, 10)
        assert expected is True, 'Previously downloaded file is displayed.'

        expected = exists(DownloadManager.Downloads.FILE_MOVED_OR_MISSING, 10)
        assert expected is True, 'Previously downloaded file has status: \'File moved or missing\'.'

    def teardown(self):
        downloads_cleanup()
