# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from moziris.api.mouse import mouse
from targets.firefox.firefox_ui.helpers.download_manager_utils import *
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Malicious warning.',
        locale=['en-US'],
        test_case_id='99498',
        test_suite_id='1827',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        malicious_file_download_library = Pattern('malicious_file_download_library.png')

        if OSHelper.is_windows():
            download_available = False
        else:
            download_available = True

        navigate('https://testsafebrowsing.appspot.com')

        expected = exists(DownloadFiles.MALICIOUS, 10)
        assert expected is True, 'Malicious file has been found.'

        width, height = DownloadFiles.MALICIOUS.get_size()

        download_file(DownloadFiles.MALICIOUS.target_offset(width / 2 + 10, 0), DownloadFiles.OK,
                      expect_accept_download_available=download_available)

        expected = exists(DownloadManager.DownloadsPanel.BLOCKED_DOWNLOAD_ICON, 10)
        assert expected is True, 'Blocked download icon is displayed.'

        expected = exists(DownloadManager.DownloadsPanel.ADD_REMOVE_DOWNLOADS_RED_ARROW, 10)
        assert expected is True, 'Open malicious download arrow is displayed.'

        expected = exists(DownloadManager.DownloadsPanel.VIRUS_OR_MALWARE_DOWNLOAD, 10)
        assert expected is True, 'Virus or malware message is displayed.'

        width, height = DownloadManager.DownloadsPanel.ADD_REMOVE_DOWNLOADS_RED_ARROW.get_size()
        arrow_location = find(DownloadManager.DownloadsPanel.ADD_REMOVE_DOWNLOADS_RED_ARROW)
        offset_arrow_location = Location(arrow_location.x + width/2 + 10, arrow_location.y)
        Mouse().move(offset_arrow_location)

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.BLOCKED_DOWNLOAD, 10)
        assert expected is True, 'Download is highlighted red.'

        click(DownloadManager.DownloadsPanel.ADD_REMOVE_DOWNLOADS_WHITE_ARROW)

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.HEADER, 10)
        assert expected is True, 'Download details header is displayed.'

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.BLOCKED_DOWNLOAD_TITLE, 10)
        assert expected is True, 'Download details title is displayed.'

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.BLOCKED_DETAILS_1, 10)
        assert expected is True, 'Download details 1 are displayed.'

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.BLOCKED_DETAILS_2, 10)
        assert expected is True, 'Download details 2 are displayed.'

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.BLOCKED_BADGE, 10)
        assert expected is True, 'Download details blocked icon is displayed.'

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.OPEN_FILE_BUTTON, 10)
        assert expected is True, 'Open file button is displayed.'

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.REMOVE_FILE_BUTTON, 10)
        assert expected is True, 'Remove file button is displayed.'

        # Open the malicious file.
        if OSHelper.is_mac():
            malicious_file = Pattern('malicious_file_name.png')
            click(DownloadManager.DownloadsPanel.DownloadDetails.OPEN_FILE_BUTTON)
            expected = exists(malicious_file, 10)
            assert expected is True, 'Malicious file is displayed.'
            click_window_control('close')

            expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
            assert expected is True, 'Download button found in the page.'

            click(NavBar.DOWNLOADS_BUTTON)
            right_click(DownloadManager.DownloadState.COMPLETED)
        else:
            click(DownloadManager.DownloadsPanel.DownloadDetails.DOWNLOADS_BACK_ARROW)
            hover(DownloadManager.SHOW_ALL_DOWNLOADS)
            expected = exists(DownloadManager.DownloadsPanel.VIRUS_OR_MALWARE_DOWNLOAD, 10)
            assert expected is True, '\'This file contains a virus or malware\' message is displayed.'
            right_click(DownloadManager.DownloadsPanel.VIRUS_OR_MALWARE_DOWNLOAD, 5)

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

        download_image_site_loaded = exists(LocalWeb.FOCUS_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert download_image_site_loaded, 'Focus site loaded'

        download_file(LocalWeb.FOCUS_LOGO, DownloadFiles.OK, max_number_of_attempts=10)

        close_tab()

        # Repeat steps 1-4 and click on Remove file.
        width, height = DownloadFiles.MALICIOUS.get_size()

        download_file(DownloadFiles.MALICIOUS.target_offset(width / 2 + 10, 0), DownloadFiles.OK,
                      expect_accept_download_available=download_available)

        expected = exists(NavBar.SEVERE_DOWNLOADS_BUTTON, 10)
        assert expected is True, 'Malicious downloads button is displayed.'

        # Remove the file from the download panel.
        click(NavBar.SEVERE_DOWNLOADS_BUTTON)

        click(DownloadManager.DownloadsPanel.ADD_REMOVE_DOWNLOADS_RED_ARROW)

        expected = exists(DownloadManager.DownloadsPanel.DownloadDetails.REMOVE_FILE_BUTTON, 10)
        assert expected is True, 'Remove file button is displayed.'

        click(DownloadManager.DownloadsPanel.DownloadDetails.REMOVE_FILE_BUTTON, 1)

        # The file is deleted from the Panel.
        type(Key.ESC)

        downloads_button = exists(NavBar.DOWNLOADS_BUTTON)
        assert downloads_button, 'Downloads button available.'

        click(NavBar.DOWNLOADS_BUTTON)

        malicious_file = exists(malicious_file_download_library)
        assert malicious_file is False, 'Malicious file is deleted from the Panel'

    def teardown(self):
        cancel_and_clear_downloads()

        downloads_cleanup()
