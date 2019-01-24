# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search on a page with small fonts'
        self.test_case_id = '127279'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        small_text_unselected_pattern = Pattern('small_text_unselected.png').similar(0.6)
        small_text_selected_pattern = Pattern('small_text_selected.png').similar(0.6)
        vertical_search_page_local = self.get_asset_path('test-findinpage.html')

        navigate(vertical_search_page_local)  # https://bug1279751.bmoattachments.org/attachment.cgi?id=8762332
        page_is_opened = exists(small_text_unselected_pattern, 10)
        assert_true(self, page_is_opened, 'The page is loaded.')

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
        small_text_unselected_exists = exists(small_text_unselected_pattern, 5)
        assert_true(self, small_text_unselected_exists, 'Small text is unselected before search')

        type('Second')
        type(Key.ENTER)

        small_text_selected_exists = exists(small_text_selected_pattern, 5)
        assert_true(self, small_text_selected_exists, 'The matching small text was found.')
