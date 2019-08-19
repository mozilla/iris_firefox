# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    def setup(self):
        jpg_file_name = 'jpgimage.jpg'
        png_file_name = 'pngimage.png'

        jpg_copy_name = 'jpgimage_bak.jpg'
        png_copy_name = 'pngimage_bak.png'

        copies_directory_name = 'copies'

        copied_jpg_file = os.path.join(copies_directory_name, jpg_copy_name)
        copied_png_file = os.path.join(copies_directory_name, png_copy_name)

        asset_dir = self.get_asset_path('')
        copies_directory_path = os.path.join(asset_dir, copies_directory_name)

        os.mkdir(copies_directory_path)

        original_jpgfile_path = self.get_asset_path(jpg_file_name)
        backup_jpgfile_path = self.get_asset_path(copied_jpg_file)

        original_png_file_path = self.get_asset_path(png_file_name)
        backup_png_file_path = self.get_asset_path(copied_png_file)

        copy_file(original_jpgfile_path, backup_jpgfile_path)
        copy_file(original_png_file_path, backup_png_file_path)

    @pytest.mark.details(
        description='Drop single and multiple .png images in demopage opened in Private Window',
        locale=['en-US'],
        test_case_id='165086',
        test_suite_id='102',
    )
    def run(self, firefox):
        library_import_backup_pattern = Library.IMPORT_AND_BACKUP_BUTTON
        library_import_restore_submenu_pattern = Library.ImportAndBackup.RESTORE
        library_import_choose_file_submenu_pattern = Library.ImportAndBackup.Restore.CHOOSE_FILE
        drop_png_file_button_pattern = Pattern('drop_png_file_button.png')
        drop_png_file_selected_button_pattern = Pattern('drop_png_file_selected_button.png')
        library_popup_pattern = Pattern('library_popup.png')
        select_bookmark_popup_pattern = Pattern('select_bookmark_tab_popup.png')
        drop_here_pattern = Pattern('drop_here.png')
        not_matching_message_pattern = Pattern('not_matching_message.png')
        matching_message_pattern = Pattern('matching_message_precise.png')
        png_bak_file_pattern = Pattern('png_bak_file.png')
        jpg_bak_file_pattern = Pattern('jpg_bak_file.png')

        if OSHelper.is_linux():
            file_type_all_files_pattern = Pattern('file_type_all_files.png')
            file_type_json_pattern = Pattern('file_type_json.png')

        drag_and_drop_duration = 2
        paste_delay = 0.5
        folderpath = self.get_asset_path('copies')

        new_private_window()

        private_window_opened = exists(PrivateWindow.private_window_pattern)
        assert private_window_opened, 'A new private window is successfully loaded.'

        navigate('https://mystor.github.io/dragndrop/')

        drop_png_data_button_displayed = exists(drop_png_file_button_pattern)
        assert drop_png_data_button_displayed, 'The demo website loaded successfully'

        click(drop_png_file_button_pattern)

        drop_png_option_selected = exists(drop_png_file_selected_button_pattern)
        assert drop_png_option_selected, 'The drop-png-file changed color to red which indicates that it ' \
                                         'has been selected.'

        matching_block_available = scroll_until_pattern_found(not_matching_message_pattern, scroll_down, (5,), 30,
                                                              paste_delay)
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

        restore_context_available = exists(library_import_restore_submenu_pattern)
        assert restore_context_available, '\'Restore\' option from \'Import and Backup\'context menu is ' \
                                          'available'

        click(library_import_restore_submenu_pattern)

        choose_file_available = exists(library_import_choose_file_submenu_pattern)
        assert choose_file_available, 'Choose file option from context menu is available'

        click(library_import_choose_file_submenu_pattern)

        select_bookmark_popup_available = exists(select_bookmark_popup_pattern)
        assert select_bookmark_popup_available, '\'Select a bookmark backup\' window is available'

        select_bookmark_popup_before = find(select_bookmark_popup_pattern)

        if OSHelper.is_mac():
            type('g', modifier=[KeyModifier.CMD, KeyModifier.SHIFT])  # open folder in Finder
            paste(folderpath)
            type(Key.ENTER)
            type('2', KeyModifier.CMD)  # change view of finder
        else:
            paste(folderpath)
            type(Key.ENTER, interval=paste_delay)

        if OSHelper.is_linux():
            json_option_available = exists(file_type_json_pattern)
            assert json_option_available, '\'File type JSON\' option in file picker window is available'

            click(file_type_json_pattern)

            all_files_option_available = exists(file_type_all_files_pattern)
            assert all_files_option_available, '\'All Files\' option in file picker window is available'

            click(file_type_all_files_pattern)

        else:
            type('*')  # Show all files in Windows Explorer
            type(Key.ENTER, interval=paste_delay)

        select_bookmark_popup_location_final = Location(Screen.SCREEN_WIDTH // 2, library_popup_tab_before.y)
        #  drag-n-drop right to prevent fails on osx
        drag_drop(select_bookmark_popup_before.right(library_title_width), select_bookmark_popup_location_final)

        test_file_png_located = exists(png_bak_file_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_file_png_located, 'PNG test file is available'

        drop_here_available = exists(drop_here_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert drop_here_available, '"Drop here" pattern is available'

        drag_drop(png_bak_file_pattern, drop_here_pattern, duration=drag_and_drop_duration)

        matching_message_displayed = exists(matching_message_pattern, region=matching_region)
        assert matching_message_displayed, 'Matching appears under the "Drop Stuff Here" area and expected ' \
                                           'result is identical to result.'

        test_file_jpg_located = exists(jpg_bak_file_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_file_jpg_located, 'JPG test file is available'

        drop_here_available = exists(drop_here_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert drop_here_available, '"Drop here" pattern is available'

        drag_drop(jpg_bak_file_pattern, drop_here_pattern, duration=drag_and_drop_duration)

        not_matching_message_displayed = exists(not_matching_message_pattern, region=not_matching_region)
        assert not_matching_message_displayed, 'Not Matching appears under the "Drop Stuff Here" area and ' \
                                               'expected result is different from result.'

        type(Key.ESC)
        close_tab()
        close_tab()

    def teardown(self):
        jpg_file_name = 'jpgimage_bak.jpg'
        png_file_name = 'pngimage_bak.png'
        copies_directory_name = 'copies'

        jpg_backup_file = os.path.join(copies_directory_name, jpg_file_name)
        png_backup_file = os.path.join(copies_directory_name, png_file_name)

        jpg_backup_path = self.get_asset_path(jpg_backup_file)
        png_backup_path = self.get_asset_path(png_backup_file)
        copies_directory = self.get_asset_path(copies_directory_name)

        delete_file(jpg_backup_path)
        delete_file(png_backup_path)
        os.rmdir(copies_directory)
