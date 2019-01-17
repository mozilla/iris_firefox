# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The downloads from a private window are not leaked to the non-private window.'
        self.test_case_id = '99475'
        self.test_suite_id = '1827'
        self.locales = ['en-US']
        self.exclude = Platform.ALL

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
        download_files_list = [DownloadFiles.MEDIUM_FILE_100MB, DownloadFiles.MEDIUM_FILE_50MB,
                               DownloadFiles.SMALL_FILE_20MB, DownloadFiles.SMALL_FILE_10MB,
                               DownloadFiles.EXTRA_SMALL_FILE_5MB]
        downloads_library_list = [DownloadFiles.LIBRARY_DOWNLOADS_5MB, DownloadFiles.LIBRARY_DOWNLOADS_10MB,
                                  DownloadFiles.LIBRARY_DOWNLOADS_20MB, DownloadFiles.LIBRARY_DOWNLOADS_50MB,
                                  DownloadFiles.LIBRARY_DOWNLOADS_100MB]

        new_private_window()
        expected = exists(PrivateWindow.private_window_pattern, 10)
        assert_true(self, expected, 'Private window successfully loaded.')

        open_downloads()

        expected = exists(DownloadManager.AboutDownloads.NO_DOWNLOADS, 10)
        assert_true(self, expected, 'The downloads category is brought to view and the following message is displayed '
                                    'in the tab: \'There are no downloads\'.')

        # Perform 5 downloads of your choice and go to the Downloads category from the Library.
        new_tab()
        navigate('https://www.thinkbroadband.com/download')

        scroll_down(15)
        for pattern in download_files_list:
            download_file(pattern, DownloadFiles.OK)
            click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

        open_library()
        expected = exists(Library.TITLE, 10)
        assert_true(self, expected, 'Library successfully opened.')

        click(Library.DownloadLibrary.DOWNLOADS)

        # Check that all the downloads are successful and displayed in the Downloads category.
        for pattern in downloads_library_list:
            expected = exists(pattern, 50)
            assert_true(self, expected, '%s file found in the Library, Downloads section.'
                        % str(pattern.get_filename()).replace('_library_downloads.png', ''))

        click_window_control('close')
        close_window()

        # In the non-private window, open the Downloads Panel and the Downloads category from the Library.
        open_library()
        expected = exists(Library.TITLE, 10)
        assert_true(self, expected, 'Library successfully opened.')

        click(Library.DownloadLibrary.DOWNLOADS)

        # Check that downloads from the private window are not displayed in non private window.
        for pattern in downloads_library_list:
            expected = exists(pattern, 2)
            assert_false(self, expected, '%s file not found in the Library, Downloads section.'
                         % str(pattern.get_filename()).replace('_library_downloads.png', ''))

        click_window_control('close')

        auto_hide_download_button()

        expected = exists(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Downloads button found in the non private window.')

        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON)
        expected = exists(DownloadManager.DownloadsPanel.NO_DOWNLOADS_FOR_THIS_SESSION, 10)
        assert_true(self, expected, 'There are no downloads displayed in the Downloads Panel.')

    def teardown(self):
        downloads_cleanup()
