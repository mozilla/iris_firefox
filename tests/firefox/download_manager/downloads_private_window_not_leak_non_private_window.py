# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.firefox_ui.helpers.customize_utils import auto_hide_download_button
from targets.firefox.firefox_ui.helpers.download_manager_utils import *
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The downloads from a private window are not leaked to the non-private window.',
        locale=['en-US'],
        test_case_id='99475',
        test_suite_id='1827',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.download.dir': PathManager.get_downloads_dir(),
                     'browser.download.folderList': 2,
                     'browser.download.useDownloadDir': True,
                     'browser.warnOnQuit': False,
                     'extensions.privatebrowsing.notification': True}
    )
    def run(self, firefox):
        download_files_list = [DownloadFiles.MEDIUM_FILE_100MB, DownloadFiles.MEDIUM_FILE_50MB,
                               DownloadFiles.SMALL_FILE_20MB, DownloadFiles.SMALL_FILE_10MB,
                               DownloadFiles.EXTRA_SMALL_FILE_5MB]
        downloads_library_list = [DownloadFiles.LIBRARY_DOWNLOADS_5MB, DownloadFiles.LIBRARY_DOWNLOADS_10MB,
                                  DownloadFiles.LIBRARY_DOWNLOADS_20MB, DownloadFiles.LIBRARY_DOWNLOADS_50MB,
                                  DownloadFiles.LIBRARY_DOWNLOADS_100MB]

        new_private_window()
        expected = exists(PrivateWindow.private_window_pattern, 10)
        assert expected is True, 'Private window successfully loaded.'

        open_downloads()

        expected = exists(DownloadManager.AboutDownloads.NO_DOWNLOADS, 10)
        assert expected is True, 'The downloads category is brought to view and the following message is displayed '
        'in the tab: \'There are no downloads\'.'

        # Perform 5 downloads of your choice and go to the Downloads category from the Library.
        new_tab()
        navigate(LocalWeb.THINKBROADBAND_TEST_SITE)

        for pattern in download_files_list:
            download_file(pattern, DownloadFiles.OK)
            file_index = download_files_list.index(pattern)

            if file_index == 0:
                expected = exists(NavBar.DOWNLOADS_BUTTON, 10)
        assert expected is True, 'Download button found in the page.'

        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

        open_library()
        expected = exists(Library.TITLE, 10)
        assert expected is True, 'Library successfully opened.'

        click(Library.DOWNLOADS)

        # Check that all the downloads are successful and displayed in the Downloads category.
        for pattern in downloads_library_list:
            expected = exists(pattern, 50)
            assert expected is True, '%s file found in the Library, Downloads section.' \
                                     % str(pattern.get_filename()).replace('_library_downloads.png', '')

        click_window_control('close')
        close_window()

        # In the non-private window, open the Downloads Panel and the Downloads category from the Library.
        open_library()
        expected = exists(Library.TITLE, 10)
        assert expected is True, 'Library successfully opened.'

        click(Library.DOWNLOADS)

        # Check that downloads from the private window are not displayed in non private window.
        for pattern in downloads_library_list:
            expected = exists(pattern, 2)
            assert expected is False, '%s file not found in the Library, Downloads section.' \
                                      % str(pattern.get_filename()).replace('_library_downloads.png', '')

        click_window_control('close')

        auto_hide_download_button()

        expected = exists(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON, 10)
        assert expected is True, 'Downloads button found in the non private window.'

        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON)
        expected = exists(DownloadManager.DownloadsPanel.NO_DOWNLOADS_FOR_THIS_SESSION, 10)
        assert expected is True, 'There are no downloads displayed in the Downloads Panel.'

    def teardown(self):
        downloads_cleanup()
