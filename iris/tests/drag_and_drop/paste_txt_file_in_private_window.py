# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Paste .txt File in demopage opened in Private Window'
        self.test_case_id = '165091'
        self.test_suite_id = '102'
        self.locales = ['en-US']
        self.blocked_by = {'id': '1288773', 'platform': Platform.ALL}

    def run(self):
        paste_txt_button_pattern = Pattern('paste_txt_file_button.png')
        paste_txt_file_selected_button_pattern = Pattern('paste_txt_file_selected_button.png')
        drop_here_pattern = Pattern('drop_here.png')
        not_matching_message_pattern = Pattern('not_matching_message.png')
        matching_message_pattern = Pattern('matching_message_precise.png')
        txt_file_pattern = Pattern('txt_file.png')
        jpg_file_pattern = Pattern('jpg_file.png')

        drag_and_drop_duration = 3
        folderpath = self.get_asset_path('')

        new_private_window()

        private_window_opened = exists(PrivateWindow.private_window_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, private_window_opened, 'A new private window is successfully loaded.')

        navigate('https://mystor.github.io/dragndrop/')

        paste_txt_file_button_displayed = exists(paste_txt_button_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, paste_txt_file_button_displayed, 'The demo website loaded successfully')

        click(paste_txt_button_pattern)

        paste_txt_option_selected = exists(paste_txt_file_selected_button_pattern)
        assert_true(self, paste_txt_option_selected, 'The paste-txt-file changed color to red which indicates that it '
                                                     'has been selected.')

        matching_block_available = scroll_until_pattern_found(not_matching_message_pattern, scroll, (-25,), 20, 1)
        assert_true(self, matching_block_available, 'The drop result verification area is displayed on the page')

        not_matching_message_location = find(not_matching_message_pattern)
        not_matching_message_width, not_matching_message_height = not_matching_message_pattern.get_size()
        not_matching_region = Region(x=not_matching_message_location.x, y=not_matching_message_location.y,
                                     width=not_matching_message_width, height=not_matching_message_height)

        matching_message_width, matching_message_height = matching_message_pattern.get_size()
        matching_region = Region(x=not_matching_message_location.x, y=not_matching_message_location.y,
                                 width=matching_message_width + 10, height=matching_message_height * 2)

        select_file_in_folder(folderpath, txt_file_pattern, edit_copy)

        drop_here_available = exists(drop_here_pattern)
        assert_true(self, drop_here_available, '"Drop here" pattern available')

        click(drop_here_pattern, drag_and_drop_duration)

        edit_paste()

        matching_message_displayed = exists(matching_message_pattern, in_region=matching_region)
        assert_true(self, matching_message_displayed, 'Matching appears under the "Drop Stuff Here" area and expected'
                                                      'result is identical to result. ')

        select_file_in_folder(folderpath, jpg_file_pattern, edit_copy)

        drop_here_available = exists(drop_here_pattern)
        assert_true(self, drop_here_available, '"Drop here" pattern available')

        click(drop_here_pattern, drag_and_drop_duration)

        edit_paste()

        not_matching_message_displayed = exists(not_matching_message_pattern, in_region=not_matching_region)
        assert_true(self, not_matching_message_displayed, 'Not Matching appears under the "Drop Stuff Here" area and '
                                                          'expected result is different from result.')

        type(Key.ESC)

        close_tab()
