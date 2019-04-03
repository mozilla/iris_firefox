# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Download panel informs the user if a former download has been deleted.'
        self.test_case_id = '99481'
        self.test_suite_id = '1827'
        self.locales = ['en-US']
        self.blocked_by = {'id': '1513494', 'platform': [Platform.LINUX]}

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
        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        download_file(DownloadFiles.EXTRA_SMALL_FILE_5MB, DownloadFiles.OK)

        expected = exists(NavBar.DOWNLOADS_BUTTON_BLUE, 10)
        assert_true(self, expected, 'Downloads button found.')

        expected = exists(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED, 10)
        assert_true(self, expected, 'Small size file download is completed.')

        expected = exists(DownloadManager.DownloadsPanel.OPEN_DOWNLOAD_FOLDER, 10)
        assert_true(self, expected, 'Containing folder button is available.')

        # Navigate to Downloads folder.
        click(DownloadManager.DownloadsPanel.OPEN_DOWNLOAD_FOLDER)

        expected = exists(DownloadManager.DOWNLOADS_FOLDER, 10)
        assert_true(self, expected, 'Downloads folder is displayed.')

        expected = exists(DownloadFiles.FOLDER_VIEW_5MB_HIGHLIGHTED, 10)
        assert_true(self, expected, 'Downloaded file is found.')

        delete_selected_file()

        try:
            expected = wait_vanish(DownloadFiles.FOLDER_VIEW_5MB_HIGHLIGHTED, 10)
            assert_true(self, expected, 'The file was successfully deleted.')
        except FindError:
            raise FindError('The file was not deleted.')

        # Close download folder window.
        click_window_control('close')

        try:
            expected = wait_vanish(DownloadManager.DOWNLOADS_FOLDER, 10)
            assert_true(self, expected, 'The downloads folder was closed.')
        except FindError:
            raise FindError('The downloads folder was not closed.')

        # Switch the focus on firefox browser.
        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Download button found in the page.')

        click(NavBar.DOWNLOADS_BUTTON.target_offset(-70, 15))

        click(NavBar.DOWNLOADS_BUTTON)

        expected = exists(DownloadManager.Downloads.EXTRA_SMALL_FILE_5MB_ZIP, 10)
        assert_true(self, expected, 'Previously downloaded file is displayed.')

        expected = exists(DownloadManager.Downloads.FILE_MOVED_OR_MISSING, 10)
        assert_true(self, expected, 'Previously downloaded file has status: \'File moved or missing\'.')

    def teardown(self):
        # Cancel all 'in progress' downloads.
        cancel_and_clear_downloads()
        # Refocus the firefox window.
        exists(LocationBar.STAR_BUTTON_UNSTARRED, 10)
        click(LocationBar.STAR_BUTTON_UNSTARRED.target_offset(+30, 0))

        downloads_cleanup()
