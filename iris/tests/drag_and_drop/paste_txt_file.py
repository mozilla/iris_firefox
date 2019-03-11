# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Paste .txt File in demopage'
        self.test_case_id = '165090'
        self.test_suite_id = '102'
        self.locales = ['en-US']
        # self.blocked_by = {'id': '1288773', 'platform': Platform.ALL}

    def run(self):
        paste_txt_button_pattern = Pattern('paste_txt_file_button.png')
        paste_txt_file_selected_button_pattern = Pattern('paste_txt_file_selected_button.png')
        drop_here_pattern = Pattern('drop_here.png')
        not_matching_message_pattern = Pattern('not_matching_message.png')
        matching_message_pattern = Pattern('matching_message_precise.png')
        txt_file_pattern = Pattern('txt_file.png')
        jpg_file_pattern = Pattern('jpg_file.png')

        if Settings.is_linux():
            file_type_all_files_pattern = Pattern('file_type_all_files.png')
            file_type_json_pattern = Pattern('file_type_json.png')

        DRAG_AND_DROP_DURATION = 3
        PASTE_DELAY = 0.5
        folderpath = self.get_asset_path('')

        navigate('https://mystor.github.io/dragndrop/')

        paste_txt_file_button_displayed = exists(paste_txt_button_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, paste_txt_file_button_displayed, 'The demo website loaded successfully')

        click(paste_txt_button_pattern)

        paste_txt_option_selected = exists(paste_txt_file_selected_button_pattern)
        assert_true(self, paste_txt_option_selected, 'The paste-txt-file changed color to red which indicates that it '
                                                     'has been selected.')

        matching_block_available = scroll_until_pattern_found(not_matching_message_pattern, scroll, (-25,), 20,
                                                              DEFAULT_UI_DELAY)
        assert_true(self, matching_block_available, 'The drop result verification area is displayed on the page')

        not_matching_message_location = find(not_matching_message_pattern)
        not_matching_message_width, not_matching_message_height = not_matching_message_pattern.get_size()
        not_matching_region = Region(x=not_matching_message_location.x, y=not_matching_message_location.y,
                                     width=not_matching_message_width, height=not_matching_message_height)

        matching_message_width, matching_message_height = matching_message_pattern.get_size()
        matching_region = Region(x=not_matching_message_location.x, y=not_matching_message_location.y,
                                 width=matching_message_width + 10, height=matching_message_height * 2)

        open_directory(folderpath)

        finder_window_loaded = exists(MainWindow.MAIN_WINDOW_CONTROLS)
        assert_true(self, finder_window_loaded, 'Finder/Explorer window successfully loaded')

        if Settings.is_mac():
            type('g', modifier=KeyModifier.CMD + KeyModifier.SHIFT)  # open folder in Finder
            paste(folderpath)
            type(Key.ENTER)
            type('2', KeyModifier.CMD)  # change view of finder
        else:
            paste(folderpath)
            type(Key.ENTER, interval=PASTE_DELAY)

        if Settings.is_linux():
            json_option_available = exists(file_type_json_pattern)
            assert_true(self, json_option_available, '\'File type JSON\' option in file picker window available')

            click(file_type_json_pattern)

            all_files_option_available = exists(file_type_all_files_pattern)
            assert_true(self, all_files_option_available, '\'All Files\' option in file picker window available')

            click(file_type_all_files_pattern)

        elif Settings.is_windows():
            type('*')  # Show all files in Windows Explorer
            type(Key.ENTER, interval=PASTE_DELAY)

        finder_window_location = find(MainWindow.MAIN_WINDOW_CONTROLS)
        finder_window_before = Location(finder_window_location.x + 10, finder_window_location.y)
        finder_window_after = Location(SCREEN_WIDTH / 2, finder_window_location.y)

        drag_drop(finder_window_before, finder_window_after)

        test_file_txt_located = exists(txt_file_pattern)
        assert_true(self, test_file_txt_located, 'TXT test file is available')

        click(txt_file_pattern)

        edit_copy()

        drop_here_available = exists(drop_here_pattern)
        assert_true(self, drop_here_available, '"Drop here" pattern available')

        click(drop_here_pattern, DRAG_AND_DROP_DURATION)

        edit_paste()

        change_window_view()

        # matching_message_displayed = exists(matching_message_pattern, in_region=matching_region)
        # assert_true(self, matching_message_displayed, 'Matching appears under the "Drop Stuff Here" area and expected '
        #                                               'result is identical to result. ')

        test_file_jpg_located = exists(jpg_file_pattern)
        assert_true(self, test_file_jpg_located, 'JPG test file is available')

        click(jpg_file_pattern)

        edit_copy()

        drop_here_available = exists(drop_here_pattern)
        assert_true(self, drop_here_available, '"Drop here" pattern available')

        click(drop_here_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)

        edit_paste()

        # not_matching_message_displayed = exists(not_matching_message_pattern, in_region=not_matching_region)
        # assert_true(self, not_matching_message_displayed, 'Not Matching appears under the "Drop Stuff Here" area and '
        #                                                   'expected result is different from result.')

        type(Key.ESC)

        change_window_view()
        close_tab()
