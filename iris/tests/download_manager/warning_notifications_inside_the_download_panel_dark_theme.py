# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bug - Warning notifications inside the Download Panel are not visible in Dark Theme.'
        self.test_case_id = '224367'
        self.test_suite_id = '1827'
        self.blocked_by = {'id': '1468453', 'platform': Platform.ALL}
        self.blocked_by = {'id': '1491614', 'platform': Platform.ALL}
        self.blocked_by = {'id': '2920', 'platform': Platform.ALL}
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

        click_hamburger_menu_option('Customize...')

        region_bottom_half = Screen.BOTTOM_HALF

        expected = region_bottom_half.exists(Customize.THEMES_DEFAULT_SET, 10)
        assert_true(self, expected, 'Themes button is available.')

        click(Customize.THEMES_DEFAULT_SET)

        expected = region_bottom_half.exists(Customize.DARK_THEME_OPTION, 10)
        assert_true(self, expected, 'Dark theme option is available.')

        click(Customize.DARK_THEME_OPTION)

        expected = region_bottom_half.exists(Customize.DARK_THEME_SET, 10)
        assert_true(self, expected, 'Dark theme is set.')

        close_customize_page()

        navigate('http://testsafebrowsing.appspot.com/s/content.exe')

        try:
            wait(DownloadFiles.SAVE_FILE, 90)
            logger.debug('The \'Save file\' option is present in the page.')
            click(DownloadFiles.SAVE_FILE)
        except FindError:
            raise FindError('The \'Save file\' option is not present in the page, aborting.')

        if Settings.get_os() != Platform.WINDOWS:
            try:
                wait(DownloadFiles.OK, 10)
                logger.debug('The OK button found in the page.')
                click(DownloadFiles.OK)
            except FindError:
                raise FindError('The OK button is not found in the page.')

        region_upper_right = Screen.UPPER_RIGHT_CORNER.top_half()

        expected = region_upper_right.exists(
            DownloadManager.DownloadsPanel.VIRUS_OR_MALWARE_DOWNLOAD_DARK_THEME.similar(0.99), 10)
        assert_true(self, expected, 'The warning message is clearly displayed in red color.')

        expected = region_upper_right.exists(DownloadManager.SHOW_ALL_DOWNLOADS_DARK_THEME.similar(0.99), 10)
        assert_true(self, expected, '\'Show All Downloads \' is clearly displayed in white color.')

    def teardown(self):
        downloads_cleanup()
