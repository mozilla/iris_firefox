# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.firefox_ui.helpers.download_manager_utils import *
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Uncommon warning..',
        locale=['en-US'],
        test_case_id='107720',
        test_suite_id='1827',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        uncommon_file_download_library = Pattern('uncommon_file_download_library.png')

        navigate('https://testsafebrowsing.appspot.com')

        expected = exists(DownloadFiles.UNCOMMON_HTTPS, 10)
        assert expected is True, 'Uncommon file has been found.'

        width, height = DownloadFiles.UNCOMMON_HTTPS.get_size()
        download_file(DownloadFiles.UNCOMMON_HTTPS.target_offset(width / 2 + 10, 0), DownloadFiles.OK)

        expected = exists(DownloadManager.DownloadsPanel.UNCOMMON_DOWNLOAD_ICON, 10)
        assert expected is True, 'Uncommon download icon is displayed.'

        expected = exists(DownloadManager.DownloadsPanel.UNCOMMON_DOWNLOAD, 10)
        assert expected is True, 'Uncommon message is displayed.'

        click(DownloadManager.DownloadsPanel.ADD_REMOVE_DOWNLOADS_ARROW)

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.HEADER, 10)
        assert expected is True, 'Download details header is displayed.'

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.UNCOMMON_DOWNLOAD_TITLE, 10)
        assert expected is True, 'Download details title is displayed.'

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.UNCOMMON_DETAILS_1, 10)
        assert expected is True, 'Download details 1 are displayed.'

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.BLOCKED_DETAILS_2, 10)
        assert expected is True, 'Download details 2 are displayed.'

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.UNWANTED_BADGE, 10)
        assert expected is True, 'Download details uncommon icon is displayed.'

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.OPEN_FILE_BUTTON, 10)
        assert expected is True, 'Open file button is displayed.'

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.REMOVE_FILE_BUTTON, 10)
        assert expected is True, 'Remove file button is displayed.'

        # Open the uncommon file.
        if OSHelper.is_mac():
            uncommon_file = Pattern('uncommon_file_name.png')
            click(DownloadManager.DownloadsPanel.DownloadDetails.OPEN_FILE_BUTTON)
            expected = exists(uncommon_file, 10)
            assert expected is True, 'Uncommon file is displayed.'
            click_window_control('close')

            expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
            assert expected is True, 'Download button found in the page.'

            click(NavBar.DOWNLOADS_BUTTON)
            right_click(DownloadManager.DownloadState.COMPLETED)
        else:
            click(DownloadManager.DownloadsPanel.DownloadDetails.DOWNLOADS_BACK_ARROW)
            hover(DownloadManager.SHOW_ALL_DOWNLOADS)
            expected = exists(DownloadManager.DownloadsPanel.UNCOMMON_DOWNLOAD, 10)
            assert expected is True, '\'The file is not commonly downloaded.\' message is displayed.'
            right_click(DownloadManager.DownloadsPanel.UNCOMMON_DOWNLOAD)

        # Clear the download panel.
        expected = exists(DownloadManager.DownloadsContextMenu.REMOVE_FROM_HISTORY, 10)
        assert expected is True, '\'Remove from history\' option is available.'

        click(DownloadManager.DownloadsContextMenu.REMOVE_FROM_HISTORY)

        # Delete downloads folder
        downloads_cleanup()

        # Use a dirty profile with at least one previous downloaded item!
        download_image = self.get_asset_path('download_image.html')

        new_tab()
        navigate(download_image)

        type(Key.ESC)

        download_image_site_loaded = exists(LocalWeb.FOCUS_LOGO)
        assert download_image_site_loaded, 'Focus site loaded'

        download_file(LocalWeb.FOCUS_LOGO, DownloadFiles.OK)

        close_tab()

        # Repeat steps 1-4 and click on Remove file.
        download_file(DownloadFiles.UNCOMMON_HTTPS.target_offset(width / 2 + 10, 0), DownloadFiles.OK)

        expected = exists(NavBar.UNWANTED_DOWNLOADS_BUTTON, 10)
        assert expected is True, 'Uncommon downloads button is displayed.'

        # Remove the file from the download panel.
        click(NavBar.UNWANTED_DOWNLOADS_BUTTON)

        click(DownloadManager.DownloadsPanel.ADD_REMOVE_DOWNLOADS_ARROW)

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.REMOVE_FILE_BUTTON, 10)
        assert expected is True, 'Remove file button is displayed.'

        click(DownloadManager.DownloadsPanel.DownloadDetails.REMOVE_FILE_BUTTON)

        # The file is deleted from the Panel.
        type(Key.ESC)

        downloads_button = exists(NavBar.DOWNLOADS_BUTTON)
        assert downloads_button, 'Downloads button available.'

        click(NavBar.DOWNLOADS_BUTTON)

        uncommon_file = exists(uncommon_file_download_library)
        assert uncommon_file is False, 'Uncommon file is deleted from the Panel'

    def teardown(self):
        downloads_cleanup()
