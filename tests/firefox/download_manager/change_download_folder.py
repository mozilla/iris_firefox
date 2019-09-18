# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.download_manager import DownloadManager
from targets.firefox.firefox_ui.helpers.download_manager_utils import DownloadFiles, downloads_cleanup, download_file
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Changing the download folder works accordingly.',
        locale=['en-US'],
        test_case_id='99488',
        test_suite_id='1827',
        blocked_by={'id': '1554158', 'platform': OSPlatform.ALL},
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        # Wait for the page to be loaded.
        try:
            wait(DownloadFiles.EXTRA_SMALL_FILE_5MB, 10)
            logger.debug('File is present in the page.')
        except FindError:
            raise FindError('File is not present in the page.')

        download_file(DownloadFiles.EXTRA_SMALL_FILE_5MB, DownloadFiles.OK)

        expected = exists(NavBar.DOWNLOADS_BUTTON_BLUE, 10)
        assert expected is True, 'Downloads button found.'

        click(NavBar.HOME_BUTTON.target_offset(70, 0))

        # Navigate to about:preferences.
        navigate('about:preferences#search')

        expected = exists(AboutPreferences.ABOUT_PREFERENCE_SEARCH_PAGE_PATTERN, 10)
        assert expected is True, 'The \'about:preferences#search\' page successfully loaded.'

        expected = exists(AboutPreferences.FIND_IN_OPTIONS, 10)
        assert expected is True, '\'Find in Options\' search field is displayed.'

        click(AboutPreferences.FIND_IN_OPTIONS)
        paste('downloads')

        expected = exists(AboutPreferences.DOWNLOADS, 10)
        assert expected is True, 'The \'Downloads\' section is displayed.'

        click(AboutPreferences.BROWSE)
        expected = exists(AboutPreferences.DOWNLOADS, 10)
        assert expected is True, '\'New Folder\' button is displayed.'

        click(Utils.NEW_FOLDER)
        expected = exists(Utils.NEW_FOLDER_HIGHLIGHTED, 10)
        assert expected is True, '\'New Folder\' is highlighted.'

        paste('new_downloads_folder')
        type(Key.ENTER)

        expected = exists(Utils.NEW_DOWNLOADS_FOLDER_HIGHLIGHTED, 10)
        assert expected is True, '\'New Downloads Folder\' is created.'

        expected = exists(Utils.SELECT_FOLDER, 10)
        assert expected is True, '\'Select Folder\' option is available.'

        click(Utils.SELECT_FOLDER)

        try:
            expected = wait_vanish(Utils.SELECT_FOLDER, 10)
            assert expected is True, 'Downloads folder option window is dismissed.'
        except FindError:
            logger.error('Downloads folder option is still displayed.')

        time.sleep(10)

        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        # Wait for the page to be loaded.
        try:
            wait(DownloadFiles.SMALL_FILE_10MB, 10)
            logger.debug('File is present in the page.')
        except FindError:
            raise FindError('File is not present in the page.')

        download_file(DownloadFiles.SMALL_FILE_10MB, DownloadFiles.OK)

        expected = exists(NavBar.DOWNLOADS_BUTTON_BLUE, 10)
        assert expected is True, 'Downloads button turns blue.'

        click(NavBar.DOWNLOADS_BUTTON_BLUE)

        expected = exists(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED, 10)
        assert expected is True, 'The 5MB download is complete.'

        file_5_mb = find(DownloadFiles.DOWNLOADS_PANEL_5MB_COMPLETED)
        region_5_mb = Region(file_5_mb.x, file_5_mb.y - 10, 500, 50)
        expected = region_5_mb.exists(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER, 10)
        assert expected is True, 'Containing folder icon is available for 5mb file.'

        region_5_mb.click(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER)

        # Workaround to avoid 1513494 bug on Linux.
        if OSHelper.is_linux():
            click(Pattern('linux_folder_icon.png'))

        expected = exists(DownloadManager.DOWNLOADS_FOLDER, 10)
        assert expected is True, 'Default Downloads folder is displayed.'

        expected = exists(DownloadFiles.FOLDER_VIEW_5MB_HIGHLIGHTED, 10)
        assert expected is True, 'Downloaded file is found.'

        close_tab()

        # Refocus the firefox window.
        click(NavBar.HOME_BUTTON.target_offset(70, 0))

        click(NavBar.DOWNLOADS_BUTTON_BLUE)

        expected = exists(DownloadFiles.DOWNLOADS_PANEL_10MB_COMPLETED.similar(0.7), 10)
        assert expected is True, 'The 10MB download is complete.'

        file_10_mb = find(DownloadFiles.DOWNLOADS_PANEL_10MB_COMPLETED)
        region_10_mb = Region(file_10_mb.x, file_10_mb.y - 10, 500, 50)
        expected = region_10_mb.exists(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER, 10)
        assert expected is True, 'Containing folder icon is available for 10mb file.'

        region_10_mb.click(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER)

        # Workaround to avoid 1513494 bug on Linux.
        if OSHelper.is_linux():
            click(Pattern('linux_folder_icon.png'))

        expected = exists(DownloadManager.NEW_DOWNLOADS_FOLDER, 10)
        assert expected is True, 'New Downloads folder is displayed.'

        expected = exists(DownloadFiles.FOLDER_VIEW_10MB_HIGHLIGHTED, 10)
        assert expected is True, '10mb file is displayed in the newly downloads folder.'

        close_tab()

        # Refocus the firefox window.
        click(NavBar.HOME_BUTTON.target_offset(70, 0))

    def teardown(self):
        downloads_cleanup()
