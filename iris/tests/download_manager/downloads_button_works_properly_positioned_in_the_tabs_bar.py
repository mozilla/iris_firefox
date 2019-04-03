# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The downloads button works properly positioned in the tabs bar.'
        self.test_case_id = '99473'
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
        download_files_list = [DownloadFiles.SMALL_FILE_20MB, DownloadFiles.SMALL_FILE_10MB,
                               DownloadFiles.EXTRA_SMALL_FILE_5MB]
        downloads_library_list = [DownloadFiles.LIBRARY_DOWNLOADS_20MB, DownloadFiles.LIBRARY_DOWNLOADS_10MB,
                                  DownloadFiles.LIBRARY_DOWNLOADS_5MB_HIGHLIGHTED]

        click_hamburger_menu_option('Customize...')

        expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Download button is available.')

        drag_drop(NavBar.DOWNLOADS_BUTTON, NavBar.BAR, 0.5)

        close_customize_page()

        expected = exists(NavBar.CUSTOM_DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Custom Download button is available in tabs bar.')

        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        for pattern in download_files_list:
            download_file(pattern, DownloadFiles.OK)

        expected = exists(NavBar.CUSTOM_DOWNLOADS_BUTTON_BLUE, 30)
        assert_true(self, expected, 'Download button turns blue when download is completed.')

        open_downloads()
        
        if Settings.get_os() == Platform.LINUX:
            drag_drop(Library.TITLE, DownloadFiles.EXTRA_SMALL_FILE_5MB, 2)

        expected = exists(NavBar.CUSTOM_DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Download button turns back to default color.')

        # Check that all downloads are displayed in Downloads category.
        for pattern in downloads_library_list:
            expected = exists(pattern, 50)
            assert_true(self, expected, '%s file found in the Library, Downloads section.'
                        % str(pattern.get_filename()).split('_')[0])

        click_window_control('close')
        close_window()

    def teardown(self):
        downloads_cleanup()
