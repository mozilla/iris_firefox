# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Remove the downloads folder.'
        self.test_case_id = '99491'
        self.test_suite_id = '1827'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        self.set_profile_pref({'browser.download.dir': IrisCore.get_downloads_dir()})
        self.set_profile_pref({'browser.download.folderList': 2})
        self.set_profile_pref({'browser.download.useDownloadDir': True})
        return

    def run(self):

        completed_5mb_file_pattern = Pattern('completed_5mb_file.png')
        missing_5mb_file_pattern = Pattern('moved_missing_5mb_file.png')
        missing_10mb_file_pattern = Pattern('moved_missing_10mb_file.png')
        missing_20mb_file_pattern = Pattern('moved_missing_20mb_file.png')

        navigate('https://www.thinkbroadband.com/download')
        download_files_list = [DownloadFiles.SMALL_FILE_20MB, DownloadFiles.SMALL_FILE_10MB,
                               DownloadFiles.EXTRA_SMALL_FILE_5MB]

        scroll(5)
        for f in download_files_list:
            download_file(f, DownloadFiles.OK)
            click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

        click(NavBar.DOWNLOADS_BUTTON)
        click(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER)

        if Settings.get_os() == Platform.LINUX:
            click(Pattern('linux_folder_icon.png'))

        expected = exists(DownloadManager.DOWNLOADS_FOLDER, 10)
        assert_true(self, expected, 'Downloads folder is displayed.')

        # Delete the downloads folder
        force_delete_folder(IrisCore.get_downloads_dir())
        click_window_control('close')

        click(NavBar.DOWNLOADS_BUTTON)

        time.sleep(DEFAULT_UI_DELAY_LONG)
        downloads_button = find(NavBar.DOWNLOADS_BUTTON)

        file_20_mb = find(DownloadFiles.DOWNLOAD_FILE_NAME_20MB)
        region_20_mb = Region(file_20_mb.x - 10, file_20_mb.y,
                              downloads_button.x - file_20_mb.x, 100)
        expected = region_20_mb.exists(DownloadManager.DownloadState.MISSING_FILE, 10)
        assert_true(self, expected, '20 MB file removed.')

        file_10_mb = find(DownloadFiles.DOWNLOAD_FILE_NAME_10MB)
        region_10_mb = Region(file_10_mb.x - 10, file_10_mb.y,
                              downloads_button.x - file_10_mb.x, file_20_mb.y - file_10_mb.y)
        expected = region_10_mb.exists(DownloadManager.DownloadState.MISSING_FILE, 10)
        assert_true(self, expected, '10 MB file was removed.')

        file_5_mb = find(DownloadFiles.DOWNLOAD_FILE_NAME_5MB)
        region_5_mb = Region(file_5_mb.x - 10, file_5_mb.y,
                             downloads_button.x - file_5_mb.x, file_10_mb.y - file_5_mb.y)
        expected = region_5_mb.exists(DownloadManager.DownloadState.MISSING_FILE, 10)
        assert_true(self, expected, '5 MB file removed.')

        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

        download_file(DownloadFiles.EXTRA_SMALL_FILE_5MB, DownloadFiles.OK)

        click(NavBar.DOWNLOADS_BUTTON)

        expected = exists(missing_20mb_file_pattern, 10)
        assert_true(self, expected, 'Missing 20 MB file is displayed.')
        expected = exists(missing_10mb_file_pattern, 10)
        assert_true(self, expected, 'Missing 10 MB file is displayed.')
        expected = exists(completed_5mb_file_pattern, 10)
        assert_true(self, expected, 'Completed 5 MB file is displayed.')
        expected = exists(missing_5mb_file_pattern, 10)
        assert_true(self, expected, 'Missing 5 MB file is displayed.')

        click(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER)
        expected = exists(DownloadManager.DOWNLOADS_FOLDER, 10)
        assert_true(self, expected, 'Downloads folder was recreated.')

        if Settings.get_os() == Platform.LINUX:
            click(Pattern('linux_folder_icon.png'))

        # Assert the newly created downloads folder
        expected = exists(DownloadManager.DOWNLOADS_FOLDER, 10)
        assert_true(self, expected, 'Downloads folder was recreated.')
        click_window_control('close')

        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

    def teardown(self):
        downloads_cleanup()
