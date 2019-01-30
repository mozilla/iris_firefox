# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '"about:downloads" displays accurate data.'
        self.test_case_id = '99487'
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
        downloads_library_list = [DownloadFiles.LIBRARY_DOWNLOADS_5MB_HIGHLIGHTED, DownloadFiles.LIBRARY_DOWNLOADS_10MB,
                                  DownloadFiles.LIBRARY_DOWNLOADS_20MB]

        navigate('https://www.thinkbroadband.com/download')

        scroll_down(20)
        for pattern in download_files_list:
            download_file(pattern, DownloadFiles.OK)
            click(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON.target_offset(-50, 0))

        # Open the Library - Downloads section.
        open_downloads()
        expected = exists(Library.TITLE, 10)
        assert_true(self, expected, 'Library successfully opened.')

        # Check that all the downloads are successful and displayed in the Downloads category from the Library.
        for pattern in downloads_library_list:
            expected = exists(pattern, 10)
            assert_true(self, expected, '%s file found in the Library, Downloads section.'
                        % str(pattern.get_filename()).split('_')[0])

        click_window_control('close')

        # Check that all the downloads are also displayed in the 'about:downloads' page.
        new_tab()
        navigate('about:downloads')
        for pattern in downloads_library_list:
            expected = exists(pattern, 10)
            assert_true(self, expected, '%s file found in the \'about:downloads\' page.'
                        % str(pattern.get_filename()).split('_')[0])

    def teardown(self):
        downloads_cleanup()
