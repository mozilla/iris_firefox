# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from iris.api.core import mouse
from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Clear Download History.'
        self.test_case_id = '99483'
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
        download_files_list = [DownloadFiles.SMALL_FILE_10MB, DownloadFiles.EXTRA_SMALL_FILE_5MB]
        downloads_library_list = [DownloadFiles.LIBRARY_DOWNLOADS_5MB, DownloadFiles.LIBRARY_DOWNLOADS_10MB]

        navigate('https://www.thinkbroadband.com/download')

        scroll_down(20)
        for pattern in download_files_list:
            download_file(pattern, DownloadFiles.OK)
            click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

        # Open the Downloads Panel and select Show All Downloads.
        expected = exists(NavBar.DOWNLOADS_BUTTON_BLUE, 10)
        assert_true(self, expected, '\'Downloads\' button found.')
        mouse.mouse_move(Location(SCREEN_WIDTH / 4 + 100, SCREEN_HEIGHT / 4))
        click(NavBar.DOWNLOADS_BUTTON_BLUE)

        expected = exists(DownloadManager.SHOW_ALL_DOWNLOADS, 10)
        assert_true(self, expected, '\'Show all downloads\' button found.')
        click(DownloadManager.SHOW_ALL_DOWNLOADS)

        expected = exists(Library.DownloadLibrary.DOWNLOADS, 10)
        assert_true(self, expected, 'The Downloads button is displayed in the Library.')
        click(Library.DownloadLibrary.DOWNLOADS)

        # Check that all the downloads are successful and displayed in the Downloads category.
        for pattern in downloads_library_list:
            expected = exists(pattern, 10)
            assert_true(self, expected, '%s file found in the Library, Downloads section.'
                        % str(pattern.get_filename()).replace('_library_downloads.png', ''))

        right_click(DownloadFiles.LIBRARY_DOWNLOADS_5MB)
        type(text='d')

        # Check that all the downloads are removed from the Library.
        for pattern in downloads_library_list:
            try:
                expected = wait_vanish(pattern, 5)
                assert_true(self, expected, '%s file not found in the Library, Downloads section.'
                            % str(pattern.get_filename()).replace('_library_downloads.png', ''))
            except FindError:
                raise FindError('Downloads are still present in the Library.')

        click_window_control('close')

        # Check that there are no downloads displayed in the 'about:downloads' page.
        navigate('about:downloads')
        expected = exists(DownloadManager.AboutDownloads.NO_DOWNLOADS, 10)
        assert_true(self, expected, 'There are no downloads displayed in the \'about:downloads\' page.')

    def teardown(self):
        downloads_cleanup()
