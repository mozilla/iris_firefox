# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.helpers.download_manager_utils import *
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='\'Open Download Folder\' opens the folder which Firefox is set to save its downloads.',
        locale=['en-US'],
        test_case_id='99480',
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

        # Workaround to avoid 1513494 bug on Linux.
        if OSHelper.is_linux():
            click(Pattern('linux_folder_icon.png'))

        expected = exists(DownloadManager.DOWNLOADS_FOLDER, 10)
        assert expected is True, 'Downloads folder is displayed.'

        expected = exists(DownloadFiles.FOLDER_VIEW_5MB_HIGHLIGHTED, 10)
        assert expected is True, 'Downloaded file is found.'

        # Close download folder window.
        close_tab()

        # Switch the focus on firefox browser.
        click(NavBar.FORWARD_BUTTON.target_offset(-50, 0))

        # Cancel all 'in progress' downloads.
        cancel_and_clear_downloads()
        # Refocus the firefox window.
        exists(LocationBar.STAR_BUTTON_UNSTARRED, 10)
        click(LocationBar.STAR_BUTTON_UNSTARRED.target_offset(+30, 0))

    def teardown(self):
        downloads_cleanup()
