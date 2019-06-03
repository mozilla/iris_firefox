# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.download_manager import DownloadManager
from targets.firefox.firefox_ui.helpers.download_manager_utils import DownloadFiles, downloads_cleanup, download_file, \
    cancel_and_clear_downloads, cancel_in_progress_downloads_from_the_library
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='"about:downloads" displays accurate data.',
        locale=['en-US'],
        test_case_id='99487',
        test_suite_id='1827',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False}
    )
    def run(self, firefox):
        download_files_list = [DownloadFiles.SMALL_FILE_20MB, DownloadFiles.SMALL_FILE_10MB,
                               DownloadFiles.EXTRA_SMALL_FILE_5MB]
        downloads_library_list = [DownloadFiles.LIBRARY_DOWNLOADS_5MB_HIGHLIGHTED, DownloadFiles.LIBRARY_DOWNLOADS_10MB,
                                  DownloadFiles.LIBRARY_DOWNLOADS_20MB]

        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        for pattern in download_files_list:
            download_file(pattern, DownloadFiles.OK)
            file_index = download_files_list.index(pattern)

            if file_index == 0:
                expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
                assert expected is True, 'Download button found in the page.'

            click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

        # Open the Library - Downloads section.
        open_downloads()
        expected = exists(Library.TITLE, 10)
        assert expected is True, 'Library successfully opened.'

        # Check that all the downloads are successful and displayed in the Downloads category from the Library.
        for pattern in downloads_library_list:
            expected = exists(pattern, 10)
            assert expected is True, (
                    '%s file found in the Library, Downloads section.' % str(pattern.get_filename()))

        click_window_control('close')

        # Check that all the downloads are also displayed in the 'about:downloads' page.
        new_tab()
        navigate('about:downloads')

        try:
            wait(DownloadFiles.LIBRARY_DOWNLOADS_20MB, 10)
            logger.debug('The page successfully loaded.')
        except FindError:
            raise FindError('The page did not load, aborting.')

        for pattern in downloads_library_list:
            if pattern == DownloadFiles.LIBRARY_DOWNLOADS_5MB_HIGHLIGHTED.similar(0.75):
                # Sometimes the 5MB file is highlighted and sometimes not. Focusing it to make the test case stable.
                click(DownloadFiles.LIBRARY_DOWNLOADS_20MB)
                repeat_key_up(3)

            expected = exists(pattern, 10)
            assert expected is True, '%s file found in the \'about:downloads\' page.' % str(pattern.get_filename())

        close_tab()

        # Cancel all 'in progress' downloads.
        cancel_in_progress_downloads_from_the_library()

    def teardown(self):
        # Remove downloads folder
        downloads_cleanup()
