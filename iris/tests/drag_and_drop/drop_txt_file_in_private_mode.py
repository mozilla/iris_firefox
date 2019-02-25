# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Drop single and multiple .txt files in demopage opened in Private Window.'
        self.test_case_id = '165079'
        self.test_suite_id = '102'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        original_txtfile_path = self.get_asset_path('testfile.txt')
        backup_txtfile_path = self.get_asset_path('testfile_bak.txt')

        original_jpgfile_path = self.get_asset_path('jpgimage.jpg')
        backup_jpgfile_path = self.get_asset_path('jpgimage_bak.jpg')

        shutil.copy(original_txtfile_path, backup_txtfile_path)
        shutil.copy(original_jpgfile_path, backup_jpgfile_path)

    def run(self):
        library_import_backup_pattern = Library.IMPORT_AND_BACKUP_BUTTON
        drop_txt_file_button_pattern = Pattern('drop_txt_file_button.png')
        drop_txt_file_selected_button_pattern = Pattern('drop_txt_file_selected_button.png')
        library_popup_pattern = Pattern('library_popup.png')
        select_bookmark_popup_pattern = Pattern('select_bookmark_tab_popup.png')
        drop_here_pattern = Pattern('drop_here.png')
        not_matching_message_pattern = Pattern('not_matching_message.png')
        matching_message_pattern = Pattern('matching_message.png')
        jpg_bak_file_pattern = Pattern('jpg_bak_file.png')
        txt_bak_file_pattern = Pattern('txt_bak_file.png')
        if Settings.is_linux():
            file_type_all_files_pattern = Pattern('file_type_all_files.png')
            file_type_json_pattern = Pattern('file_type_json.png')

        folderpath = self.get_asset_path('')
        original_txtfile_path = self.get_asset_path('testfile.txt')

        new_private_window()

        private_window_opened = exists(PrivateWindow.private_window_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, private_window_opened, 'A new private window is successfully loaded.')

        navigate('https://mystor.github.io/dragndrop/')

        drop_html_data_button_displayed = exists(drop_txt_file_button_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, drop_html_data_button_displayed, 'The demo website loaded successfully')

        click(drop_txt_file_button_pattern)

        drop_txt_option_selected = exists(drop_txt_file_selected_button_pattern)
        assert_true(self, drop_txt_option_selected, 'The drop-txt-file changed color to red which indicates that it '
                                                    'has been selected.')

        matching_block_available = scroll_until_pattern_found(not_matching_message_pattern, scroll, (-25,), 20,
                                                              DEFAULT_UI_DELAY)
        assert_true(self, matching_block_available, 'The drop result verification area is present on the page')

        open_library()

        # open and drag library window
        library_popup_open = exists(library_import_backup_pattern.similar(0.6), DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, library_popup_open, 'Library popup window is correctly opened.')

        library_popup_tab_before = find(library_popup_pattern)
        library_title_width, library_title_height = library_popup_pattern.get_size()
        library_tab_region_before = Region(library_popup_tab_before.x,
                                           library_popup_tab_before.y,
                                           library_title_width, library_title_height)
        library_popup_tab_after = Location(SCREEN_WIDTH/2, library_popup_tab_before.y)

        drag_drop(library_popup_tab_before, library_popup_tab_after, DEFAULT_DELAY_BEFORE_DROP)
        wait_vanish(library_popup_pattern, in_region=library_tab_region_before)

        click(library_import_backup_pattern)

        restore_context = exists(Library.ImportAndBackup.RESTORE)
        assert_true(self, restore_context, '\'Restore\' option from \'Import and Backup\'context menu available')

        click(Library.ImportAndBackup.RESTORE)

        choose_file = exists(Library.ImportAndBackup.Restore.CHOOSE_FILE)
        assert_true(self, choose_file, 'Choose file option from context menu available')

        click(Library.ImportAndBackup.Restore.CHOOSE_FILE)

        select_bookmark_popup = exists(select_bookmark_popup_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, select_bookmark_popup, '\'Select a bookmark backup\' window available')

        select_bookmark_popup_before = find(select_bookmark_popup_pattern)

        if Settings.is_mac():
            type('g', modifier=KeyModifier.CMD + KeyModifier.SHIFT)  # go to folder
            paste(folderpath)
            type(Key.ENTER)
        else:
            paste(folderpath)
            type(Key.ENTER, interval=DEFAULT_UI_DELAY)

        if Settings.is_linux():
            json_option = exists(file_type_json_pattern)
            assert_true(self, json_option, '\'File type JSON\' option in file picker window available')

            click(file_type_json_pattern)

            all_files_option = exists(file_type_all_files_pattern)
            assert_true(self, all_files_option, '\'All Files\' option in file picker window available')

            click(file_type_all_files_pattern)

        else:
            type('*')
            type(Key.ENTER, interval=DEFAULT_UI_DELAY)

        select_bookmark_popup_after = Location(SCREEN_WIDTH / 2, library_popup_tab_before.y)

        drag_drop(select_bookmark_popup_before.right(30), select_bookmark_popup_after)

        test_file_txt = exists(txt_bak_file_pattern)
        assert_true(self, test_file_txt, 'TXT test file is available')

        drop_here = exists(drop_here_pattern)
        assert_true(self, drop_here, '"Drop here" pattern available')

        drag_drop(txt_bak_file_pattern, drop_here_pattern)

        matching_message_displayed = exists(matching_message_pattern)
        assert_true(self, matching_message_displayed, 'Matching appears under the "Drop Stuff Here" area and expected '
                                                      'result is identical to result.')

        test_file_jpg = exists(jpg_bak_file_pattern)
        assert_true(self, test_file_jpg, 'JPG test file is available')

        drag_drop(jpg_bak_file_pattern, drop_here_pattern)

        not_matching_message_displayed = exists(not_matching_message_pattern)
        assert_true(self, not_matching_message_displayed, 'Not Matching appears under the "Drop Stuff Here" area and '
                                                          'expected result is different from result.')

        type(Key.ESC)
        close_tab()

    def teardown(self):
        jpg_backup_path = self.get_asset_path('jpgimage_bak.jpg')
        os.remove(jpg_backup_path)
        txt_backup_path = self.get_asset_path('testfile_bak.txt')
        os.remove(txt_backup_path)
