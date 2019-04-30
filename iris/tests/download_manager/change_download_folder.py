# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Changing the download folder works accordingly.'
        self.test_case_id = '99488'
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
        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        # Wait for the page to be loaded.
        try:
            wait(DownloadFiles.EXTRA_SMALL_FILE_5MB, 10)
            logger.debug('File is present in the page.')
        except FindError:
            raise FindError('File is not present in the page.')

        download_file(DownloadFiles.EXTRA_SMALL_FILE_5MB, DownloadFiles.OK)

        expected = exists(NavBar.DOWNLOADS_BUTTON_BLUE, 10)
        assert_true(self, expected, 'Downloads button found.')

        click(NavBar.HOME_BUTTON.target_offset(70, 0))

        # Navigate to about:preferences.
        navigate('about:preferences#search')

        expected = exists(AboutPreferences.ABOUT_PREFERENCE_SEARCH_PAGE_PATTERN, 10)
        assert_true(self, expected, 'The \'about:preferences#search\' page successfully loaded.')

        expected = exists(AboutPreferences.FIND_IN_OPTIONS, 10)
        assert_true(self, expected, '\'Find in Options\' search field is displayed.')

        click(AboutPreferences.FIND_IN_OPTIONS)
        paste('downloads')

        expected = exists(AboutPreferences.DOWNLOADS, 10)
        assert_true(self, expected, 'The \'Downloads\' section is displayed.')

        click(AboutPreferences.BROWSE)
        expected = exists(AboutPreferences.DOWNLOADS, 10)
        assert_true(self, expected, '\'New Folder\' button is displayed.')

        click(Utils.NEW_FOLDER)
        expected = exists(Utils.NEW_FOLDER_HIGHLIGHTED, 10)
        assert_true(self, expected, '\'New Folder\' is highlighted.')

        paste('new_downloads_folder')
        type(Key.ENTER)

        expected = exists(Utils.NEW_DOWNLOADS_FOLDER_HIGHLIGHTED, 10)
        assert_true(self, expected, '\'New Downloads Folder\' is created.')

        click(Utils.SELECT_FOLDER)

        try:
            expected = wait_vanish(Utils.SELECT_FOLDER, 10)
            assert_true(self, expected, 'Downloads folder option window is dismissed.')
        except FindError:
            logger.error('Downloads folder option is still displayed.')

        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        # Wait for the page to be loaded.
        try:
            wait(DownloadFiles.SMALL_FILE_10MB, 10)
            logger.debug('File is present in the page.')
        except FindError:
            raise FindError('File is not present in the page.')

        download_file(DownloadFiles.SMALL_FILE_10MB, DownloadFiles.OK)

        expected = exists(NavBar.DOWNLOADS_BUTTON_BLUE, 10)
        assert_true(self, expected, 'Downloads button turns blue.')

        click(NavBar.DOWNLOADS_BUTTON_BLUE)

        expected = exists(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED, 10)
        assert_true(self, expected, 'The 5MB download is complete.')

        file_5_mb = find(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED)
        region_5_mb = Region(file_5_mb.x, file_5_mb.y - 10, 500, 50)
        expected = region_5_mb.exists(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER, 10)
        assert_true(self, expected, 'Containing folder icon is available for 5mb file.')

        click(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER, in_region=region_5_mb)

        # Workaround to avoid 1513494 bug on Linux.
        if Settings.get_os() == Platform.LINUX:
            click(Pattern('linux_folder_icon.png'))

        expected = exists(DownloadManager.DOWNLOADS_FOLDER, 10)
        assert_true(self, expected, 'Default Downloads folder is displayed.')

        expected = exists(DownloadFiles.FOLDER_VIEW_5MB_HIGHLIGHTED, 10)
        assert_true(self, expected, 'Downloaded file is found.')

        close_tab()

        # Refocus the firefox window.
        click(NavBar.HOME_BUTTON.target_offset(70, 0))

        click(NavBar.DOWNLOADS_BUTTON_BLUE)

        expected = exists(DownloadFiles.DOWNLOADS_PANEL_10MB_COMPLETED.similar(0.7), 10)
        assert_true(self, expected, 'The 10MB download is complete.')

        file_10_mb = find(DownloadFiles.DOWNLOADS_PANEL_10MB_COMPLETED)
        region_10_mb = Region(file_10_mb.x, file_10_mb.y - 10, 500, 50)
        expected = region_10_mb.exists(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER, 10)
        assert_true(self, expected, 'Containing folder icon is available for 10mb file.')

        click(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER, in_region=region_10_mb)

        # Workaround to avoid 1513494 bug on Linux.
        if Settings.get_os() == Platform.LINUX:
            click(Pattern('linux_folder_icon.png'))

        expected = exists(DownloadManager.NEW_DOWNLOADS_FOLDER, 10)
        assert_true(self, expected, 'New Downloads folder is displayed.')

        expected = exists(DownloadFiles.FOLDER_VIEW_10MB_HIGHLIGHTED, 10)
        assert_true(self, expected, '10mb file is displayed in the newly downloads folder.')

        close_tab()

        # Refocus the firefox window.
        click(NavBar.HOME_BUTTON.target_offset(70, 0))

    def teardown(self):
        # Set back default downloads folder.
        navigate('about:preferences#search')

        paste('downloads')
        click(AboutPreferences.BROWSE)

        if Settings.get_os() == Platform.MAC:
            click(DownloadManager.NEW_DOWNLOADS_FOLDER)
        if Settings.get_os() == Platform.LINUX:
            click(DownloadManager.DOWNLOADS_FOLDER_PATH)
        else:
            click(DownloadManager.DOWNLOADS_FOLDER)

        click(Utils.SELECT_FOLDER)
        downloads_cleanup()
