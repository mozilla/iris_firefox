# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *
from os import system
from shutil import copyfile

class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Drop .txt File in demopage'
        self.test_case_id = '165078'
        self.test_suite_id = '1828'
        self.locales = ['en-US']

    def run(self):
        library_import_backup_pattern = Library.IMPORT_AND_BACKUP_BUTTON
        drop_txt_file_button_pattern = Pattern('drop_txt_file_button.png')
        test_file_txt_pattern = Pattern('textfile_txt.png')
        jpgimage_title_pattern = Pattern('jpgimage_title.png')
        library_popup_pattern = Pattern('library_popup.png')
        select_bookmark_popup_pattern = Pattern('select_bookmark_tab_popup.png')
        drop_here_pattern = Pattern('drop_here.png')
        matching_message_pattern = Pattern('matching_message.png')
        not_matching_message_pattern = Pattern('not_matching_message.png')

        filepath = self.get_asset_path('')
        test_bookmarks_path = self.get_asset_path('testfile_bak.txt')
        testfile_bookmarks_path = self.get_asset_path('testfile.txt')

        shutil.copy(testfile_bookmarks_path, test_bookmarks_path)

        navigate('https://mystor.github.io/dragndrop/')

        drop_html_data_button_displayed = exists(drop_txt_file_button_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, drop_html_data_button_displayed, 'Site downloaded')

        click(drop_txt_file_button_pattern)

        open_library()

        # drag library window
        library_popup_open = exists(library_import_backup_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, library_popup_open, 'Library is correctly opened.')

        library_popup_tab_before = find(library_popup_pattern)
        library_popup_tab_after = Location(SCREEN_WIDTH/2, library_popup_tab_before.y)

        drag_drop(library_popup_tab_before, library_popup_tab_after)

        click(library_import_backup_pattern)

        restore_context = exists(Library.ImportAndBackup.RESTORE)
        assert_true(self, restore_context, 'Restore context button available' )
        click(Library.ImportAndBackup.RESTORE)

        choose_file = exists(Library.ImportAndBackup.Restore.CHOOSE_FILE)
        assert_true(self, choose_file, 'Choose file option available')
        click(Library.ImportAndBackup.Restore.CHOOSE_FILE)

        select_bookmark_popup = exists(select_bookmark_popup_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, select_bookmark_popup, 'select_bookmark_popup')

        select_bookmark_popup_before = find(select_bookmark_popup_pattern)
        select_bookmark_popup_after = Location(SCREEN_WIDTH / 2, library_popup_tab_before.y)
        drag_drop(select_bookmark_popup_before, select_bookmark_popup_after)

        if Settings.is_mac():
            type('g', modifier=KeyModifier.CMD + KeyModifier.SHIFT)  # go to folder
            paste(test_bookmarks_path)
            type(Key.ENTER)
        else:
            paste(filepath )
            type(Key.ENTER, interval=DEFAULT_UI_DELAY)

        type('*')
        type(Key.ENTER, interval=DEFAULT_UI_DELAY)

        test_file_txt = exists(test_file_txt_pattern)
        assert_true(self, test_file_txt, 'txt test file is available')

        drop_here = exists(drop_here_pattern)
        assert_true(self, drop_here, '"Drop here" pattern available')

        drag_drop(test_file_txt_pattern, drop_here_pattern)

        matching_message_displayed = exists(matching_message_pattern)
        assert_true(self, matching_message_displayed, 'The data is matching')

        jpgimage_title = exists(jpgimage_title_pattern)
        assert_true(self, jpgimage_title, 'jpgimage_title')
        find(jpgimage_title_pattern)

        drag_drop(jpgimage_title_pattern, drop_here_pattern)

        not_matching_message_displayed = exists(not_matching_message_pattern)
        assert_true(self, not_matching_message_displayed, 'The data is not matching')

        close_window()

    def teardown(self):
        test_bookmarks_path = self.get_asset_path('testfile_bak.txt')
        os.remove(test_bookmarks_path)
