# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.api.core.firefox_ui.private_window import PrivateWindow
from iris.api.helpers.customize_utils import auto_hide_download_button
from iris.api.helpers.download_manager_utils import download_file, DownloadFiles
from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The downloads from a private window are not leaked to the non-private window.'
        self.test_case_id = '99475'
        self.test_suite_id = '1827'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        return

    def run(self):
        # Open a private window.
        new_private_window()
        expected = exists(PrivateWindow.private_window_pattern, 10)
        assert_true(self, expected, 'Private window successfully loaded.')

        # Open the Library and select Downloads.
        open_downloads()

        expected = exists(DownloadManager.PrivateDownloadManager.NO_DOWNLOADS, 10)
        assert_true(self, expected, 'The downloads category is brought to view and the following message is displayed '
                                    'in the tab: \'There are no downloads\'.')

        # Perform 5 downloads of your choice and go to the Downloads category from the Library.
        new_tab()
        navigate('https://www.thinkbroadband.com/download')

        # Close the Downloads panel after each download to increase the test execution.
        download_file(self, DownloadFiles.MEDIUM_FILE_100MB, DownloadFiles.OK, '100MB')
        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-100, 15))
        download_file(self, DownloadFiles.MEDIUM_FILE_50MB, DownloadFiles.OK, '50MB')
        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-100, 15))
        download_file(self, DownloadFiles.SMALL_FILE_20MB, DownloadFiles.OK, '20MB')
        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-100, 15))
        download_file(self, DownloadFiles.SMALL_FILE_10MB, DownloadFiles.OK, '10MB')
        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-100, 15))
        download_file(self, DownloadFiles.EXTRA_SMALL_FILE_5MB, DownloadFiles.OK, '5MB')
        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-100, 15))

        open_library()
        expected = exists(Library.TITLE, 10)
        assert_true(self, expected, 'Library successfully opened.')

        click(Library.DOWNLOADS)

        # Check that all the downloads are successful and displayed in the Downloads category.
        expected = exists(DownloadFiles.LIBRARY_DOWNLOADS_5MB, 10)
        assert_true(self, expected, '5MB file found in the Library, Downloads section.')
        expected = exists(DownloadFiles.LIBRARY_DOWNLOADS_10MB, 10)
        assert_true(self, expected, '10MB file found in the Library, Downloads section.')
        expected = exists(DownloadFiles.LIBRARY_DOWNLOADS_20MB, 10)
        assert_true(self, expected, '20MB file found in the Library, Downloads section.')
        expected = exists(DownloadFiles.LIBRARY_DOWNLOADS_50MB, 10)
        assert_true(self, expected, '50MB file found in the Library, Downloads section.')
        expected = exists(DownloadFiles.LIBRARY_DOWNLOADS_100MB, 10)
        assert_true(self, expected, '100MB file found in the Library, Downloads section.')

        # Close the Library and the private window.
        click_window_control('close')
        close_window()

        # In the non-private window, open the Downloads Panel and the Downloads category from the Library.
        open_library()
        expected = exists(Library.TITLE, 10)
        assert_true(self, expected, 'Library successfully opened.')

        click(Library.DOWNLOADS)

        # Check that downloads from the private window are not displayed in non private window.
        expected = exists(DownloadFiles.LIBRARY_DOWNLOADS_5MB, 2)
        assert_false(self, expected, '5MB file not found in the Library, Downloads section.')
        expected = exists(DownloadFiles.LIBRARY_DOWNLOADS_10MB, 2)
        assert_false(self, expected, '10MB file not found in the Library, Downloads section.')
        expected = exists(DownloadFiles.LIBRARY_DOWNLOADS_20MB, 2)
        assert_false(self, expected, '20MB file not found in the Library, Downloads section.')
        expected = exists(DownloadFiles.LIBRARY_DOWNLOADS_50MB, 2)
        assert_false(self, expected, '50MB file not found in the Library, Downloads section.')
        expected = exists(DownloadFiles.LIBRARY_DOWNLOADS_100MB, 2)
        assert_false(self, expected, '100MB file not found in the Library, Downloads section.')

        # Close the Library.
        click_window_control('close')

        # Enable the download button in the non private window.
        auto_hide_download_button(self)

        expected = exists(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Downloads button found in the non private window.')

        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON)
        expected = exists(DownloadManager.DownloadsPanel.NO_DOWNLOADS_FOR_THIS_SESSION, 10)
        assert_true(self, expected, 'There are no downloads displayed in the Downloads Panel.')
