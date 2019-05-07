# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Download warnings can be customized or disabled from the UI.'
        self.test_case_id = '99477'
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
        # Navigate to about:preferences.
        navigate('about:preferences#search')

        expected = exists(AboutPreferences.ABOUT_PREFERENCE_SEARCH_PAGE_PATTERN, 10)
        assert_true(self, expected, 'The \'about:preferences#search\' page successfully loaded.')

        expected = exists(AboutPreferences.FIND_IN_OPTIONS, 10)
        assert_true(self, expected, '\'Find in Options\' search field is displayed.')

        click(AboutPreferences.FIND_IN_OPTIONS)
        paste('dangerous')

        expected = exists(AboutPreferences.DECEPTIVE_CONTENT_AND_DANGEROUS_SOFTWARE, 10)
        assert_true(self, expected, 'Deceptive content and dangerous software section is displayed.')

        expected = exists(AboutPreferences.BLOCK_DANGEROUS_DOWNLOADS, 10)
        assert_true(self, expected, '\'Block dangerous downloads\' option is available.')
        expected = exists(AboutPreferences.WARN_UNWANTED_UNCOMMON_SOFTWARE, 10)
        assert_true(self, expected, '\'Warm you about unwanted and uncommon software\' option is available.')

        option_1 = find(AboutPreferences.BLOCK_DANGEROUS_AND_DECEPTIVE_CONTENT)
        region_option_1 = Region(option_1.x - 100, option_1.y - 10, 500, 40)

        if region_option_1.exists(AboutPreferences.CHECKED_BOX, 10):
            click(AboutPreferences.BLOCK_DANGEROUS_AND_DECEPTIVE_CONTENT)

        expected = region_option_1.exists(AboutPreferences.UNCHECKED_BOX, 10)
        assert_true(self, expected, '\'Block dangerous and deceptive content\' option is unchecked.')

        # expected = exists(AboutPreferences.BLOCK_DANGEROUS_DOWNLOADS_GRAYED_OUT.exact(), 10)
        # assert_true(self, expected, '\'Block dangerous downloads\' option is grayed out.')
        # expected = exists(AboutPreferences.WARN_UNWANTED_UNCOMMON_SOFTWARE_GRAYED_OUT.exact(), 10)
        # assert_false(self, expected, '\'Warm you about unwanted and uncommon software\' option is not grayed out.')

        navigate('http://testsafebrowsing.appspot.com/')

        # Download all items from Desktop Download Warning.
        expected = exists(DownloadFiles.MALICIOUS, 10)
        assert_true(self, expected, '\'"malicious" warning, based on content\' link has been found.')
        width, height = DownloadFiles.MALICIOUS.get_size()
        download_file(DownloadFiles.MALICIOUS.target_offset(width + 10, height / 2), DownloadFiles.OK)
        expected = exists(DownloadFiles.DOWNLOADS_PANEL_CONTENT_COMPLETED, 10)
        assert_true(self, expected, '\'"malicious" warning, based on content\' download file is completed.')

        expected = exists(DownloadFiles.MALICIOUS_HTTPS, 10)
        assert_true(self, expected, '\'"malicious" warning, based on content with https\' link has been found.')
        width, height = DownloadFiles.MALICIOUS_HTTPS.get_size()
        download_file(DownloadFiles.MALICIOUS_HTTPS.target_offset(width + 10, height / 2), DownloadFiles.OK)
        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Download button found in the page.')
        click(NavBar.DOWNLOADS_BUTTON)
        expected = exists(DownloadFiles.DOWNLOADS_PANEL_CONTENT1_COMPLETED, 10)
        assert_true(self, expected, '\'"malicious" warning, based on content with https\' download file is completed.')

        expected = exists(DownloadFiles.DANGEROUS_HOST_WARNING, 10)
        assert_true(self, expected, '\'"dangerous host" warning\' link has been found.')
        width, height = DownloadFiles.DANGEROUS_HOST_WARNING.get_size()
        download_file(DownloadFiles.DANGEROUS_HOST_WARNING.target_offset(width + 10, height / 2), DownloadFiles.OK)
        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Download button found in the page.')
        click(NavBar.DOWNLOADS_BUTTON)
        expected = exists(DownloadFiles.DOWNLOADS_PANEL_BADREP_COMPLETED, 10)
        assert_true(self, expected, '\'"dangerous host" warning\' download file is completed.')

        expected = exists(DownloadFiles.UNCOMMON, 10)
        assert_true(self, expected, '\'"uncommon" warning, for .exe\' link has been found.')
        width, height = DownloadFiles.UNCOMMON.get_size()
        download_file(DownloadFiles.UNCOMMON.target_offset(width + 10, height / 2), DownloadFiles.OK)
        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Download button found in the page.')
        click(NavBar.DOWNLOADS_BUTTON)
        expected = exists(DownloadFiles.DOWNLOADS_PANEL_UNKNOWN_COMPLETED, 10)
        assert_true(self, expected, '\'"uncommon" warning, for .exe\' download file is completed.')

        expected = exists(DownloadFiles.UNCOMMON_HTTPS, 10)
        assert_true(self, expected, '\'"uncommon" warning, for https .exe\' link has been found.')
        width, height = DownloadFiles.UNCOMMON_HTTPS.get_size()
        download_file(DownloadFiles.UNCOMMON_HTTPS.target_offset(width + 10, height / 2), DownloadFiles.OK)
        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Download button found in the page.')
        click(NavBar.DOWNLOADS_BUTTON)
        expected = exists(DownloadFiles.DOWNLOADS_PANEL_UNKNOWN1_COMPLETED, 10)
        assert_true(self, expected, '\'"uncommon" warning, for https .exe\' download file is completed.')

        expected = exists(DownloadFiles.POTENTIALLY_UNWANTED, 10)
        assert_true(self, expected, '\'"potentially unwanted app" warning, for .exe\' link has been found.')
        width, height = DownloadFiles.POTENTIALLY_UNWANTED.get_size()
        download_file(DownloadFiles.POTENTIALLY_UNWANTED.target_offset(width + 10, height / 2), DownloadFiles.OK)
        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Download button found in the page.')
        click(NavBar.DOWNLOADS_BUTTON)
        expected = exists(DownloadFiles.DOWNLOADS_PANEL_PUA_COMPLETED, 10)
        assert_true(self, expected, '\'"potentially unwanted app" warning, for .exe\' download file is completed.')

        # Clear All Downloads
        click(DownloadManager.SHOW_ALL_DOWNLOADS)
        expected = exists(Library.TITLE, 10)
        assert_true(self, expected, 'Library successfully opened.')
        click(Library.DownloadLibrary.CLEAR_DOWNLOADS)
        click_window_control('close')
        downloads_cleanup()

        # Navigate back to about:preferences.
        navigate('about:preferences#search')

        expected = exists(AboutPreferences.ABOUT_PREFERENCE_SEARCH_PAGE_PATTERN, 10)
        assert_true(self, expected, 'The \'about:preferences#search\' page successfully loaded.')

        expected = exists(AboutPreferences.FIND_IN_OPTIONS, 10)
        assert_true(self, expected, '\'Find in Options\' search field is displayed.')

        click(AboutPreferences.FIND_IN_OPTIONS)
        paste('dangerous')

        expected = exists(AboutPreferences.DECEPTIVE_CONTENT_AND_DANGEROUS_SOFTWARE, 10)
        assert_true(self, expected, '\'Deceptive content and dangerous software\' section is displayed.')

        expected = region_option_1.exists(AboutPreferences.UNCHECKED_BOX, 10)
        assert_true(self, expected, '\'Block dangerous and deceptive content\' option is unchecked.')

        click(AboutPreferences.BLOCK_DANGEROUS_AND_DECEPTIVE_CONTENT)
        expected = region_option_1.exists(AboutPreferences.CHECKED_BOX, 10)
        assert_true(self, expected, '\'Block dangerous and deceptive content\' option is checked.')

        option_2 = find(AboutPreferences.WARN_UNWANTED_UNCOMMON_SOFTWARE)
        click(AboutPreferences.WARN_UNWANTED_UNCOMMON_SOFTWARE)
        region_option_2 = Region(option_2.x - 100, option_2.y - 10, 500, 40)
        expected = region_option_2.exists(AboutPreferences.UNCHECKED_BOX, 10)
        assert_true(self, expected, '\'Warn you about unwanted and uncommon software\' option is unchecked.')

        navigate('http://testsafebrowsing.appspot.com/')

        # Download all items from Desktop Download Warning.
        expected = exists(DownloadFiles.MALICIOUS, 10)
        assert_true(self, expected, '\'"malicious" warning, based on content\' link has been found.')
        width, height = DownloadFiles.MALICIOUS.get_size()
        download_file(DownloadFiles.MALICIOUS.target_offset(width + 10, height / 2), DownloadFiles.OK)
        expected = exists(NavBar.SEVERE_DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Malicious downloads button is displayed.')
        click(NavBar.SEVERE_DOWNLOADS_BUTTON)
        expected = exists(DownloadManager.SHOW_ALL_DOWNLOADS, 10)
        assert_true(self, expected, 'Downloads panel is displayed.')
        downloaded_file = find(DownloadFiles.LIBRARY_DOWNLOADS_CONTENT_RED)
        region_file = Region(downloaded_file.x - 100, downloaded_file.y - 35, 500, 90)
        expected = region_file.exists(DownloadManager.DownloadsPanel.BLOCKED_DOWNLOAD_ICON, 10)
        assert_true(self, expected, 'Blocked download icon is displayed and file download is highlighted red.')

        expected = exists(DownloadFiles.MALICIOUS_HTTPS, 10)
        assert_true(self, expected, '\'"malicious" warning, based on content with https\' link has been found.')
        width, height = DownloadFiles.MALICIOUS_HTTPS.get_size()
        download_file(DownloadFiles.MALICIOUS_HTTPS.target_offset(width + 10, height / 2), DownloadFiles.OK)
        expected = exists(NavBar.SEVERE_DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Malicious downloads button is displayed.')
        click(NavBar.SEVERE_DOWNLOADS_BUTTON)
        expected = exists(DownloadManager.SHOW_ALL_DOWNLOADS, 10)
        assert_true(self, expected, 'Downloads panel is displayed.')
        downloaded_file = find(DownloadFiles.LIBRARY_DOWNLOADS_CONTENT1_RED)
        region_file = Region(downloaded_file.x - 100, downloaded_file.y - 35, 500, 90)
        expected = region_file.exists(DownloadManager.DownloadsPanel.BLOCKED_DOWNLOAD_ICON, 10)
        assert_true(self, expected, 'Blocked download icon is displayed and file download is highlighted red.')

        expected = exists(DownloadFiles.DANGEROUS_HOST_WARNING, 10)
        assert_true(self, expected, '\'"dangerous host" warning\' link has been found.')
        width, height = DownloadFiles.DANGEROUS_HOST_WARNING.get_size()
        download_file(DownloadFiles.DANGEROUS_HOST_WARNING.target_offset(width + 10, height / 2), DownloadFiles.OK)
        expected = exists(NavBar.SEVERE_DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Malicious downloads button is displayed.')
        click(NavBar.SEVERE_DOWNLOADS_BUTTON)
        expected = exists(DownloadManager.SHOW_ALL_DOWNLOADS, 10)
        assert_true(self, expected, 'Downloads panel is displayed.')
        downloaded_file = find(DownloadFiles.LIBRARY_DOWNLOADS_BADREP_RED)
        region_file = Region(downloaded_file.x - 100, downloaded_file.y - 35, 500, 90)
        expected = region_file.exists(DownloadManager.DownloadsPanel.BLOCKED_DOWNLOAD_ICON, 10)
        assert_true(self, expected, 'Blocked download icon is displayed and file download is highlighted red.')

        expected = exists(DownloadFiles.UNCOMMON, 10)
        assert_true(self, expected, '\'"uncommon" warning, for .exe\' link has been found.')
        width, height = DownloadFiles.UNCOMMON.get_size()
        download_file(DownloadFiles.UNCOMMON.target_offset(width + 10, height / 2), DownloadFiles.OK)
        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Download button found in the page.')
        click(NavBar.DOWNLOADS_BUTTON)
        expected = exists(DownloadFiles.DOWNLOADS_PANEL_UNKNOWN_COMPLETED, 10)
        assert_true(self, expected, '\'"uncommon" warning, for .exe\' download file is completed.')

        expected = exists(DownloadFiles.UNCOMMON_HTTPS, 10)
        assert_true(self, expected, '\'"uncommon" warning, for https .exe\' link has been found.')
        width, height = DownloadFiles.UNCOMMON_HTTPS.get_size()
        download_file(DownloadFiles.UNCOMMON_HTTPS.target_offset(width + 10, height / 2), DownloadFiles.OK)
        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Download button found in the page.')
        click(NavBar.DOWNLOADS_BUTTON)
        expected = exists(DownloadFiles.DOWNLOADS_PANEL_UNKNOWN1_COMPLETED, 10)
        assert_true(self, expected, '\'"uncommon" warning, for https .exe\' download file is completed.')

        expected = exists(DownloadFiles.POTENTIALLY_UNWANTED, 10)
        assert_true(self, expected, '\'"potentially unwanted app" warning, for .exe\' link has been found.')
        width, height = DownloadFiles.POTENTIALLY_UNWANTED.get_size()
        download_file(DownloadFiles.POTENTIALLY_UNWANTED.target_offset(width + 10, height / 2), DownloadFiles.OK)
        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Download button found in the page.')
        click(NavBar.DOWNLOADS_BUTTON)
        expected = exists(DownloadFiles.DOWNLOADS_PANEL_PUA_COMPLETED, 10)
        assert_true(self, expected, '\'"potentially unwanted app" warning, for .exe\' download file is completed.')

    def teardown(self):
        downloads_cleanup()
