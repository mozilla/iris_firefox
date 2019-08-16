# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    def setup(self):

        copies_directory_name = 'copies'
        asset_dir = self.get_asset_path('')
        copies_directory_path = os.path.join(asset_dir, copies_directory_name)
        os.mkdir(copies_directory_path)

        jpg_file_name = 'jpgimage.jpg'
        jpg_copy_name = 'jpgimage_bak.jpg'
        copied_jpg_file = os.path.join(copies_directory_name, jpg_copy_name)

        original_jpgfile_path = self.get_asset_path(jpg_file_name)
        backup_jpgfile_path = self.get_asset_path(copied_jpg_file)

        copy_file(original_jpgfile_path, backup_jpgfile_path)

        txt_file_name = 'testfile.txt'
        txt_copy_name = 'testfile_bak.txt'
        copied_txt_file = os.path.join(copies_directory_name, txt_copy_name)

        original_txtfile_path = self.get_asset_path(txt_file_name)
        backup_txtfile_path = self.get_asset_path(copied_txt_file)

        copy_file(original_txtfile_path, backup_txtfile_path)

    @pytest.mark.details(
        description='Drop single and multiple .txt files in demopage opened in Private Window.',
        locale=['en-US'],
        test_case_id='165086',
        test_suite_id='102',
    )
    def run(self, firefox):
        library_import_backup_pattern = Library.IMPORT_AND_BACKUP_BUTTON
        drop_txt_file_button_pattern = Pattern('drop_txt_file_button.png')
        drop_txt_file_selected_button_pattern = Pattern('drop_txt_file_selected_button.png')
        library_popup_pattern = Pattern('library_popup.png')
        select_bookmark_popup_pattern = Pattern('select_bookmark_tab_popup.png')
        drop_here_pattern = Pattern('drop_here.png')
        not_matching_message_pattern = Pattern('not_matching_message.png')
        matching_message_pattern = Pattern('matching_message_precise.png')
        jpg_bak_file_pattern = Pattern('jpg_bak_file.png')
        txt_bak_file_pattern = Pattern('txt_bak_file.png')
        file_type_all_files_pattern = None
        file_type_json_pattern = None

        if OSHelper.is_linux():
            file_type_all_files_pattern = Pattern('file_type_all_files.png')
            file_type_json_pattern = Pattern('file_type_json.png')

        folderpath = self.get_asset_path('copies')

        drag_and_drop_duration = 2
        paste_delay = 0.5
        new_private_window()

        private_window_opened = exists(PrivateWindow.private_window_pattern)
        assert private_window_opened, 'A new private window is successfully loaded.'

        navigate('https://mystor.github.io/dragndrop/')

        drop_html_data_button_displayed = exists(drop_txt_file_button_pattern)
        assert drop_html_data_button_displayed, 'The demo website loaded successfully'

        click(drop_txt_file_button_pattern)

        drop_txt_option_selected = exists(drop_txt_file_selected_button_pattern)
        assert drop_txt_option_selected, 'The drop-txt-file changed color to red which indicates that it ' \
                                         'has been selected.'

        matching_block_available = scroll_until_pattern_found(not_matching_message_pattern, scroll_down, (5,), 30, 1)
        assert matching_block_available, 'The drop result verification area is displayed on the page'

        not_matching_message_location = find(not_matching_message_pattern)
        not_matching_message_width, not_matching_message_height = not_matching_message_pattern.get_size()
        not_matching_region = Region(not_matching_message_location.x, not_matching_message_location.y,
                                     width=not_matching_message_width, height=not_matching_message_height)

        matching_message_width, matching_message_height = matching_message_pattern.get_size()
        matching_region = Region(not_matching_message_location.x, not_matching_message_location.y,
                                 width=matching_message_width + 10, height=matching_message_height * 2)

        open_library()

        # open and drag library window
        library_popup_open = exists(library_import_backup_pattern.similar(0.6))
        assert library_popup_open, 'Library popup window is correctly opened.'

        library_popup_tab_before = find(library_popup_pattern)
        library_title_width, library_title_height = library_popup_pattern.get_size()
        library_tab_region_after = Region(Screen.SCREEN_WIDTH // 2 - library_title_width // 2,
                                          library_popup_tab_before.y - library_title_height // 2,
                                          width=library_title_width * 2, height=library_title_height * 3)
        library_popup_tab_after = Location(Screen.SCREEN_WIDTH // 2, library_popup_tab_before.y)

        drag_drop(library_popup_tab_before, library_popup_tab_after, duration=drag_and_drop_duration)

        library_popup_dropped = exists(library_popup_pattern, region=library_tab_region_after)
        assert library_popup_dropped, 'Library popup dropped to right half of screen successfully'

        click(library_import_backup_pattern)

        restore_context = exists(Library.ImportAndBackup.RESTORE)
        assert restore_context, '"Restore" option from "Import and Backup"context menu available'

        click(Library.ImportAndBackup.RESTORE)

        choose_file = exists(Library.ImportAndBackup.Restore.CHOOSE_FILE)
        assert choose_file, 'Choose file option from context menu available'

        click(Library.ImportAndBackup.Restore.CHOOSE_FILE)

        select_bookmark_popup = exists(select_bookmark_popup_pattern)
        assert select_bookmark_popup, '"Select a bookmark backup" window available'

        select_bookmark_popup_before = find(select_bookmark_popup_pattern)

        if OSHelper.is_mac():
            type('g', modifier=[KeyModifier.CMD, KeyModifier.SHIFT])  # open folder in file picker
            paste(folderpath)
            type(Key.ENTER)
            type('1', KeyModifier.CMD)
        else:
            paste(folderpath)
            type(Key.ENTER, interval=paste_delay)

        if OSHelper.is_linux():
            json_option = exists(file_type_json_pattern)
            assert json_option, '"File type JSON" option in file picker window available'

            click(file_type_json_pattern)

            all_files_option = exists(file_type_all_files_pattern)
            assert all_files_option, '"All Files" option in file picker window available'

            click(file_type_all_files_pattern)

        else:
            type('*')
            type(Key.ENTER, interval=paste_delay)

        select_bookmark_popup_location_final = Location(Screen.SCREEN_WIDTH // 2, library_popup_tab_before.y)
        #  drag-n-drop right to prevent fails on osx
        drag_drop(select_bookmark_popup_before.right(library_title_width), select_bookmark_popup_location_final)

        test_file_txt = exists(txt_bak_file_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_file_txt, 'TXT test file is available'

        drop_here = exists(drop_here_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert drop_here, '"Drop here" pattern available'

        drag_drop(txt_bak_file_pattern, drop_here_pattern, duration=drag_and_drop_duration)

        matching_message_displayed = exists(matching_message_pattern, region=matching_region)
        assert matching_message_displayed, 'Matching appears under the "Drop Stuff Here" area and expected ' \
                                           'result is identical to result. '

        test_file_jpg = exists(jpg_bak_file_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_file_jpg, 'JPG test file is available'

        drag_drop(jpg_bak_file_pattern, drop_here_pattern, duration=drag_and_drop_duration)

        not_matching_message_displayed = exists(not_matching_message_pattern, region=not_matching_region)
        assert not_matching_message_displayed, 'Not Matching appears under the "Drop Stuff Here" area and ' \
                                               'expected result is different from result.'

        type(Key.ESC)
        close_tab()

    def teardown(self):
        jpg_file_name = 'jpgimage_bak.jpg'
        txt_file_name = 'testfile_bak.txt'
        copies_directory_name = 'copies'

        jpg_backup_file = os.path.join(copies_directory_name, jpg_file_name)
        txt_backup_file = os.path.join(copies_directory_name, txt_file_name)

        jpg_backup_path = self.get_asset_path(jpg_backup_file)
        txt_backup_path = self.get_asset_path(txt_backup_file)
        copies_directory = self.get_asset_path(copies_directory_name)

        delete_file(jpg_backup_path)
        delete_file(txt_backup_path)
        os.rmdir(copies_directory)
