# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Paste html data in demopage opened in Private Window'
        self.test_case_id = '165101'
        self.test_suite_id = '102'
        self.locales = ['en-US']

    def run(self):
        drop_stuff_here_area_pattern = Pattern('drop_stuff_here_area.png')
        paste_html_data_radiobutton_pattern = Pattern('paste_html_data.png')
        paste_html_data_radiobutton_selected_pattern = Pattern('paste_html_data_selected.png')
        phrase_from_wiki_page_pattern = Pattern('wiki_article_header.png')
        matching_message_pattern = Pattern('matching_message.png')
        not_matching_message_pattern = Pattern("not_matching_message.png")
        image_from_wiki_article_pattern = Pattern("image_from_wiki.png")
        copy_image_context_menu_pattern = Pattern('copy_image_option.png')

        new_private_window()
        navigate('https://mystor.github.io/dragndrop/')
        page_opened_in_private_mode = exists(paste_html_data_radiobutton_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, page_opened_in_private_mode, 'Firefox started and page loaded successfully.')

        click(paste_html_data_radiobutton_pattern)
        paste_html_data_selected = exists(paste_html_data_radiobutton_selected_pattern)
        assert_true(self, paste_html_data_selected,
                    'The \'paste-html-data\' changed color to red which indicates that it has been selected.')

        new_tab()
        select_tab(2)
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        page_opened = exists(phrase_from_wiki_page_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, page_opened, 'Web page successfully loads.')

        double_click(phrase_from_wiki_page_pattern)
        edit_copy()
        text_copied = Env.get_clipboard() == 'SOAP'
        assert_true(self, text_copied, 'The text is copied to the clipboard.')

        select_tab(1)
        drop_stuff_here_area_pattern = scroll_until_pattern_found(not_matching_message_pattern, type, (Key.PAGE_DOWN,))
        assert_true(self, drop_stuff_here_area_pattern, '\'Drop stuff here\' area is displayed on the page')

        edit_paste()
        matching_message_exists = scroll_until_pattern_found(matching_message_pattern, type, (Key.PAGE_DOWN,))
        assert_true(self, matching_message_exists,
                    '\'Matching\' appears under the \'Drop Stuff Here\' '
                    'area, the expected result is identical to the result.')

        select_tab(2)
        image_exists = exists(image_from_wiki_article_pattern)
        assert_true(self, image_exists, 'Image is displayed on the page')

        right_click(image_from_wiki_article_pattern)
        copy_image_option_available = exists(copy_image_context_menu_pattern)
        assert_true(self, copy_image_option_available,
                    '\'Copy Image\' option is available in the context menu after right clicking at the image')

        click(copy_image_context_menu_pattern)
        select_tab(1)
        edit_paste()

        not_matching_message_displayed = scroll_until_pattern_found(not_matching_message_pattern, type,
                                                                    (Key.PAGE_DOWN,))
        assert_true(self, not_matching_message_displayed, '\'Not Matching\' appears under the \'Drop Stuff Here\'' 
                                                          'area, the expected result is different from the result.')

        close_window()
        close_window()
