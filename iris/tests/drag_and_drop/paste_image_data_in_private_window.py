# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Paste image data in demopage opened in Private Window'
        self.test_case_id = '165099'
        self.test_suite_id = '102'
        self.locales = ['en-US']

    def run(self):
        paste_image_data_radiobutton_pattern = Pattern('paste_image_data.png')
        paste_image_data_radiobutton_selected_pattern = Pattern('paste_image_data_selected.png')
        matching_message_pattern = Pattern('matching_message.png')
        first_picture_pattern = Pattern("first_pocket_image.png")
        second_picture_pattern = Pattern("second_pocket_image.png")
        copy_image_context_menu_pattern = Pattern('copy_image_option.png')

        new_private_window()
        navigate('https://mystor.github.io/dragndrop/')

        page_opened_in_private_mode = exists(paste_image_data_radiobutton_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, page_opened_in_private_mode, 'Firefox started and page loaded successfully.')

        click(paste_image_data_radiobutton_pattern)
        paste_image_data_selected = exists(paste_image_data_radiobutton_selected_pattern)
        assert_true(self, paste_image_data_selected,
                    'The \'paste-image-data\' changed color to red which indicates that it has been selected.')

        new_tab()
        select_tab(2)
        navigate(LocalWeb.POCKET_TEST_SITE)
        page_opened = exists(first_picture_pattern, DEFAULT_SITE_LOAD_TIMEOUT) and exists(
                             second_picture_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, page_opened, 'Web page successfully loads.')

        right_click(first_picture_pattern)
        copy_image_option_available = exists(copy_image_context_menu_pattern)
        assert_true(self, copy_image_option_available,
                    '\'Copy Image\' option is available in the context menu after right clicking at the first image')

        click(copy_image_context_menu_pattern)
        select_tab(1)
        edit_paste()
        matching_message_appears = scroll_until_pattern_found(matching_message_pattern, type, (Key.DOWN,))
        assert_true(self, matching_message_appears,
                    '\'Matching\' appears under the \'Drop Stuff Here\' area,'
                    ' the expected result is identical to the result.')

        select_tab(2)
        right_click(second_picture_pattern)
        copy_image_option_available = exists(copy_image_context_menu_pattern)
        assert_true(self, copy_image_option_available,
                    '\'Copy Image\' option is available in the context menu after right clicking at the second image')

        click(copy_image_context_menu_pattern)
        select_tab(1)
        edit_paste()
        matching_message_appears = exists(matching_message_pattern)
        assert_true(self, matching_message_appears,
                    '\'Matching\' appears under the \'Drop Stuff Here\' area,'
                    ' the expected result is identical to the result.')

        close_window()
        close_window()
