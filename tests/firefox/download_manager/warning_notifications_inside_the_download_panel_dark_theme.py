# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.customize import Customize
from targets.firefox.firefox_ui.helpers.download_manager_utils import *
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug - Warning notifications inside the Download Panel are not visible in Dark Theme.',
        locale=['en-US'],
        test_case_id='224367',
        test_suite_id='1827',
        blocked_by={'id': '1491614', 'platform': OSPlatform.ALL},
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        click_hamburger_menu_option('Customize...')

        region_bottom_half = Screen.BOTTOM_HALF

        expected = region_bottom_half.exists(Customize.THEMES_DEFAULT_SET, 10)
        assert expected is True, 'Themes button is available.'

        click(Customize.THEMES_DEFAULT_SET)

        expected = region_bottom_half.exists(Customize.DARK_THEME_OPTION, 10)
        assert expected is True, 'Dark theme option is available.'

        click(Customize.DARK_THEME_OPTION)

        expected = region_bottom_half.exists(Customize.DARK_THEME_SET, 10)
        assert expected is True, 'Dark theme is set.'

        close_customize_page()

        navigate('http://testsafebrowsing.appspot.com/s/content.exe')

        try:
            wait(DownloadFiles.SAVE_FILE, 90)
            logger.debug('The \'Save file\' option is present in the page.')
            click(DownloadFiles.SAVE_FILE)
        except FindError:
            raise FindError('The \'Save file\' option is not present in the page, aborting.')

        if OSHelper.get_os() != OSPlatform.WINDOWS:
            try:
                wait(DownloadFiles.OK, 10)
                logger.debug('The OK button found in the page.')
                click(DownloadFiles.OK)
            except FindError:
                raise FindError('The OK button is not found in the page.')

        region_upper_right = Screen.UPPER_RIGHT_CORNER.top_half()

        expected = region_upper_right.exists(
            DownloadManager.DownloadsPanel.VIRUS_OR_MALWARE_DOWNLOAD_DARK_THEME.similar(0.99), 10)
        assert expected is True, 'The warning message is clearly displayed in red color.'

        expected = region_upper_right.exists(DownloadManager.SHOW_ALL_DOWNLOADS_DARK_THEME.similar(0.99), 10)
        assert expected is True, '\'Show All Downloads \' is clearly displayed in white color.'

    def teardown(self):
        downloads_cleanup()
