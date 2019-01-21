# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search on a page with stylized words'
        self.test_case_id = '127280'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        style_text_url_pattern = Pattern('style_text_url.png').similar(0.6)
        style_text_first_not_selected_pattern = Pattern('style_text_first_not_selected.png').similar(0.6)
        style_text_first_selected_pattern = Pattern('style_text_first_selected.png')
        style_text_second_selected_pattern = Pattern('style_text_second_selected.png')
        style_text_last_selected_pattern = Pattern('style_text_last_selected.png')

        vertical_search_page_local = self.get_asset_path('findbar_stylized.html')
        navigate(vertical_search_page_local)  # https://bug1279704.bmoattachments.org/attachment.cgi?id=8762295

        navigated_to_style_url = exists(style_text_url_pattern, 5)
        assert_true(self, navigated_to_style_url, 'Style text URL loaded successfully.')

        # to prevent selecting of all text in win 10
        delay_click = Location(500, 500)
        click(delay_click, 1)

        open_find()

        # Remove all text from the Find Toolbar

        edit_select_all()
        edit_delete()

        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, 5)
        assert_true(self, find_toolbar_is_opened, 'The Find Toolbar is successfully displayed '
                                                  'by pressing CTRL + F / Cmd + F,.')

        # Assure that text is not selected before testing
        first_text_unselected_exists = exists(style_text_first_not_selected_pattern, 5)
        assert_true(self, first_text_unselected_exists, 'Style text is unselected before search')

        type('testcase')

        first_text_selected_exists = exists(style_text_first_selected_pattern, 5)
        assert_true(self, first_text_selected_exists, 'First matching style text was found.')

        # next
        find_next()
        second_text_selected_exists = exists(style_text_second_selected_pattern, 5)
        assert_true(self, second_text_selected_exists, 'Second matching style text was found.')

        # to last
        [find_next() for _ in range(1, 10)]

        last_text_selected_exist = exists(style_text_last_selected_pattern, 5)
        assert_true(self, last_text_selected_exist, 'Last matching style text was found.')
