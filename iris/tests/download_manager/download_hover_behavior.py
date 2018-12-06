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
        self.meta = 'Hover behavior.'
        self.test_case_id = '99478'
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
        # Download a large file.
        navigate('https://www.thinkbroadband.com/download')

        download_file(DownloadFiles.VERY_LARGE_FILE_1GB, DownloadFiles.OK)
        time.sleep(DEFAULT_UI_DELAY)

        expected = exists(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Downloads button found.')

        # Open the Downloads Panel.
        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL, 10)
        assert_true(self, expected, 'X button is properly displayed.')

        # Hover the 'Close' button.
        hover(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL)
        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL_HIGHLIGHTED, 10)
        assert_true(self, expected, 'Cancel button is highlighted properly.')

        # Click the 'Close' button.
        click(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL)
        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_RETRY_HIGHLIGHTED, 10)
        assert_true(self, expected, 'Retry button is highlighted properly.')

        expected = exists(DownloadFiles.DOWNLOAD_NAME_1GB, 10)
        assert_true(self, expected, 'The downloaded file name is properly displayed.')

        # Hover the file name.
        hover(DownloadFiles.DOWNLOAD_NAME_1GB)
        expected = exists(DownloadFiles.DOWNLOAD_CANCELED, 10)
        assert_true(self, expected, 'The status and the source page are properly displayed when hovering the downloaded'
                                    ' file name.')
