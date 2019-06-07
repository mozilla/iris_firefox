# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from src.core.api.mouse import mouse
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

        navigate('https://testsafebrowsing.appspot.com')

        expected = exists(DownloadFiles.MALICIOUS, 10)
        assert expected is True, 'Malicious file has been found.'

        width, height = DownloadFiles.MALICIOUS.get_size()
        download_file(DownloadFiles.MALICIOUS.target_offset(width / 2 + 10, 0), DownloadFiles.OK)

        expected = exists(DownloadManager.DownloadsPanel.BLOCKED_DOWNLOAD_ICON, 10)
        assert expected is True, 'Blocked download icon is displayed.'

        expected = exists(DownloadManager.DownloadsPanel.ADD_REMOVE_DOWNLOADS_RED_ARROW, 10)
        assert expected is True, 'Open malicious download arrow is displayed.'

        expected = exists(DownloadManager.DownloadsPanel.VIRUS_OR_MALWARE_DOWNLOAD, 10)
        assert expected is True, 'Virus or malware message is displayed.'

        width, height = DownloadManager.DownloadsPanel.ADD_REMOVE_DOWNLOADS_RED_ARROW.get_size()
        mouse.move(DownloadManager.DownloadsPanel.ADD_REMOVE_DOWNLOADS_RED_ARROW.target_offset(width / 2 + 10, 0))

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
            right_click(DownloadManager.DownloadsPanel.VIRUS_OR_MALWARE_DOWNLOAD)

        # Clear the download panel.
        expected = exists(DownloadManager.DownloadsContextMenu.REMOVE_FROM_HISTORY, 10)
        assert expected is True, '\'Remove from history\' option is available.'
        click(DownloadManager.DownloadsContextMenu.REMOVE_FROM_HISTORY)

        # Check the malicious download button.
        width, height = DownloadFiles.MALICIOUS.get_size()
        download_file(DownloadFiles.MALICIOUS.target_offset(width / 2 + 10, 0), DownloadFiles.OK)
        expected = exists(NavBar.SEVERE_DOWNLOADS_BUTTON, 10)
        assert expected is True, 'Malicious downloads button is displayed.'

        # Remove the file from the download panel.
        click(NavBar.SEVERE_DOWNLOADS_BUTTON)
        click(DownloadManager.DownloadsPanel.ADD_REMOVE_DOWNLOADS_RED_ARROW)
        click(DownloadManager.DownloadsPanel.DownloadDetails.REMOVE_FILE_BUTTON)

        # Check that there are no downloads displayed in Downloads Library window.
        for step in open_show_all_downloads_window_from_library_menu():
            assert expected is True, (step.resolution, step.message)

        expected = exists(malicious_file_download_library, 10)
        assert expected is False, 'Malicious file was deleted from Downloads Library.'
        click_window_control('close')

        # Check that there are no downloads displayed in the 'about:downloads' page.
        navigate('about:downloads')
        expected = exists(DownloadManager.AboutDownloads.NO_DOWNLOADS, 10)
        assert expected is True, 'There are no downloads displayed in the \'about:downloads\' page.'

        # Check that there are no downloads displayed in the downloads folder.
        open_directory(PathManager.get_downloads_dir())
        expected = exists(malicious_file_download_library, 10)
        assert expected is False, 'Malicious file was deleted from the download folder.'
        click_window_control('close')

        click(DownloadManager.AboutDownloads.NO_DOWNLOADS)

    def teardown(self):
        downloads_cleanup()
