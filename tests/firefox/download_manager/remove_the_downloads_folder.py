# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.download_manager import DownloadManager
from targets.firefox.firefox_ui.helpers.download_manager_utils import DownloadFiles, downloads_cleanup, download_file, \
    force_delete_folder
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Remove the downloads folder.',
        locale=['en-US'],
        test_case_id='99491',
        test_suite_id='1827',
        blocked_by={'id': '1535006', 'platform': OSPlatform.ALL},
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)
        download_files_list = [DownloadFiles.SMALL_FILE_20MB, DownloadFiles.SMALL_FILE_10MB,
                               DownloadFiles.EXTRA_SMALL_FILE_5MB]

        for f in download_files_list:
            download_file(f, DownloadFiles.OK)
            file_index = download_files_list.index(f)

            if file_index == 0:
                expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
                assert expected is True, 'Download button found in the page.'

            click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

        click(NavBar.DOWNLOADS_BUTTON)
        expected = exists(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER, 10)
        assert expected is True, 'Containing folder button is available.'

        click(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER)

        if OSHelper.is_linux():
            click(Pattern('linux_folder_icon.png'))

        expected = exists(DownloadManager.DOWNLOADS_FOLDER, 10)
        assert expected is True, 'Downloads folder is displayed.'

        # Delete the downloads folder
        force_delete_folder(PathManager.get_downloads_dir())
        click_window_control('close')

        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert expected is True, 'Download button found in the page.'
        click(NavBar.DOWNLOADS_BUTTON)

        downloads_button = find(NavBar.DOWNLOADS_BUTTON)

        file_20_mb = find(DownloadFiles.DOWNLOAD_FILE_NAME_20MB)
        region_20_mb = Region(file_20_mb.x - 10, file_20_mb.y,
                              downloads_button.x - file_20_mb.x, 100)
        expected = region_20_mb.exists(DownloadManager.DownloadState.MISSING_FILE, 10)
        assert expected is True, '20 MB file removed.'

        file_10_mb = find(DownloadFiles.DOWNLOAD_FILE_NAME_10MB)
        region_10_mb = Region(file_10_mb.x - 10, file_10_mb.y,
                              downloads_button.x - file_10_mb.x, file_20_mb.y - file_10_mb.y)
        expected = region_10_mb.exists(DownloadManager.DownloadState.MISSING_FILE, 10)
        assert expected is True, '10 MB file was removed.'

        file_5_mb = find(DownloadFiles.DOWNLOAD_FILE_NAME_5MB)
        region_5_mb = Region(file_5_mb.x - 10, file_5_mb.y,
                             downloads_button.x - file_5_mb.x, file_10_mb.y - file_5_mb.y)
        expected = region_5_mb.exists(DownloadManager.DownloadState.MISSING_FILE, 10)
        assert expected is True, '5 MB file removed.'

        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

        download_file(DownloadFiles.EXTRA_SMALL_FILE_5MB, DownloadFiles.OK)

        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert expected is True, 'Download button found in the page.'

        click(NavBar.DOWNLOADS_BUTTON)

        expected = exists(DownloadFiles.DOWNLOADS_PANEL_20MB_MISSING.similar(0.75), 10)
        assert expected is True, 'Missing 20 MB file is displayed.'
        expected = exists(DownloadFiles.DOWNLOADS_PANEL_10MB_MISSING.similar(0.75), 10)
        assert expected is True, 'Missing 10 MB file is displayed.'
        expected = exists(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED.similar(0.75), 10)
        assert expected is True, 'Completed 5 MB file is displayed.'
        expected = exists(DownloadFiles.DOWNLOADS_PANEL_5MB_MISSING.similar(0.75), 10)
        assert expected is True, 'Missing 5 MB file is displayed.'

        click(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER)
        expected = exists(DownloadManager.DOWNLOADS_FOLDER, 10)
        assert expected is True, 'Downloads folder was recreated.'

        if OSHelper.is_linux():
            click(Pattern('linux_folder_icon.png'))

        # Assert the newly created downloads folder
        expected = exists(DownloadManager.DOWNLOADS_FOLDER, 10)
        assert expected is True, 'Downloads folder was recreated.'
        click_window_control('close')

        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

    def teardown(self):
        downloads_cleanup()
