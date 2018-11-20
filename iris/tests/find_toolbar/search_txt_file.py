# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search on a text file (.txt)'
        self.test_case_id = '127273'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):

        find_toolbar_pattern = Pattern('find_toolbar_text.png')
        txt_page_title_pattern = Pattern('txt_page_title.png')
        txt_page_title_pattern.similarity = 0.6

        text_first_occurrence_hl_pattern = Pattern('txt_text_first_occurrence_hl.png')
        text_first_occurrence_white_pattern = Pattern('txt_text_first_occurrence_white.png')
        text_second_occurrence_hl_pattern = Pattern('txt_text_second_occurrence_hl.png')
        text_second_occurrence_white_pattern = Pattern('txt_text_second_occurrence_white.png')

        test_page_local = self.get_asset_path('dmatest.txt')
        navigate(test_page_local)

        txt_page_title_pattern_exists = exists(txt_page_title_pattern, 5)

        assert_true(self, txt_page_title_pattern_exists, 'The page is successfully loaded.')

        open_find()

        # Remove all text from the Find Toolbar
        edit_select_all()
        edit_delete()

        find_toolbar_is_opened = exists(find_toolbar_pattern, 5)

        assert_true(self, find_toolbar_is_opened, 'The Find Toolbar is successfully displayed '
                                                  'by pressing CTRL + F / Cmd + F,.')

        type('Part')

        text_first_occurrence_hl_exists = exists(text_first_occurrence_hl_pattern, 5)
        text_second_occurrence_white_exists = exists(text_second_occurrence_white_pattern, 5)

        assert_true(self, (text_first_occurrence_hl_exists and text_second_occurrence_white_exists),
                    'All the matching words/characters are found.')

        text_first_occurrence_hl_exists = exists(text_first_occurrence_hl_pattern, 5)
        text_second_occurrence_white_exists = exists(text_second_occurrence_white_pattern, 5)

        assert_true(self, text_first_occurrence_hl_exists and text_second_occurrence_white_exists,
                    'First occurrence highlighted')

        # Go to next occurrence
        find_next()

        text_first_occurrence_white_exists = exists(text_first_occurrence_white_pattern, 5)
        text_second_occurrence_hl_exists = exists(text_second_occurrence_hl_pattern, 5)

        assert_true(self, text_first_occurrence_white_exists and text_second_occurrence_hl_exists,
                    'Second occurrence highlighted')

        # Get back to first occurrence
        find_previous()

        text_first_occurrence_exists_before_scroll = exists(text_first_occurrence_hl_pattern, 5)

        # Move found word away of screen and back
        for i in range(4):
            scroll_down()

        for i in range(4):
            scroll_up()

        text_first_occurrence_exists_after_scroll = exists(text_first_occurrence_hl_pattern, 5)

        assert_true(self, text_first_occurrence_exists_before_scroll and text_first_occurrence_exists_after_scroll,
                    'Occurrence exists after scroll up and down')
