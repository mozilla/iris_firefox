# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from src.core.api.mouse import mouse
from targets.firefox.firefox_ui.download_manager import DownloadManager
from targets.firefox.firefox_ui.helpers.download_manager_utils import DownloadFiles, downloads_cleanup, download_file
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Clear Download History.',
        locale=['en-US'],
        test_case_id='99483',
        test_suite_id='1827',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        download_files_list = [DownloadFiles.SMALL_FILE_10MB, DownloadFiles.EXTRA_SMALL_FILE_5MB]
        downloads_library_list = [DownloadFiles.LIBRARY_DOWNLOADS_5MB, DownloadFiles.LIBRARY_DOWNLOADS_10MB]

        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        for pattern in download_files_list:
            download_file(pattern, DownloadFiles.OK)
            file_index = download_files_list.index(pattern)

            if file_index == 0:
                expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
                assert expected is True, 'Download button found in the page.'

            click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

        # Open the Downloads Panel and select Show All Downloads.
        expected = exists(NavBar.DOWNLOADS_BUTTON_BLUE, 10)
        assert expected is True, '\'Downloads\' button found.'
        mouse.move(Location(Screen.SCREEN_WIDTH / 4 + 100, Screen.SCREEN_HEIGHT / 4))
        click(NavBar.DOWNLOADS_BUTTON_BLUE)

        expected = exists(DownloadManager.SHOW_ALL_DOWNLOADS, 10)
        assert expected is True, '\'Show all downloads\' button found.'
        click(DownloadManager.SHOW_ALL_DOWNLOADS)

        expected = exists(Library.DOWNLOADS, 10)
        assert expected is True, 'The Downloads button is displayed in the Library.'
        click(Library.DOWNLOADS)

        # Check that all the downloads are successful and displayed in the Downloads category.
        for pattern in downloads_library_list:
            expected = exists(pattern, 10)
            assert expected is True, ('%s file found in the Library, Downloads section.'
                                      % str(pattern.get_filename()).replace('_library_downloads.png', ''))

        right_click(DownloadFiles.LIBRARY_DOWNLOADS_5MB)
        type(text='d')

        # Check that all the downloads are removed from the Library.
        for pattern in downloads_library_list:
            try:
                expected = wait_vanish(pattern, 5)
                assert expected is True, ('%s file not found in the Library, Downloads section.'
                                          % str(pattern.get_filename()).replace('_library_downloads.png', ''))
            except FindError:
                raise FindError('Downloads are still present in the Library.')

        click_window_control('close')

        # Check that there are no downloads displayed in the 'about:downloads' page.
        navigate('about:downloads')
        expected = exists(DownloadManager.AboutDownloads.NO_DOWNLOADS, 10)
        assert expected is True, 'There are no downloads displayed in the \'about:downloads\' page.'

    def teardown(self):
        downloads_cleanup()
