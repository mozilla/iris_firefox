# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Navigate back and forward on a page'
        self.test_case_id = '127261'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):

        find_toolbar_pattern = Pattern('find_toolbar_text.png')
        wiki_logo = Pattern('wiki_logo_icon.png')
        arrow_back_button_pattern = Pattern('arrow_back_button.png')
        arrow_forward_button_pattern = Pattern('arrow_forward_button.png')
        new_tab_icon_pattern = Pattern('new_tab_icon.png')

        new_tab()

        test_page_local = self.get_asset_path('Wikipedia.htm')
        navigate(test_page_local)

        page_loaded = exists(wiki_logo, 20)

        assert_true(self, page_loaded, 'The website successfully loaded.')

        open_find()

        # Remove all text from the Find Toolbar
        edit_select_all()
        edit_delete()

        find_toolbar_is_opened = exists(find_toolbar_pattern, 15)
        assert_true(self, find_toolbar_is_opened, 'The find toolbar is opened')

        click(arrow_back_button_pattern, 2)
        find_toolbar_is_opened_previous_page = exists(new_tab_icon_pattern, 10)

        assert_true(self, find_toolbar_is_opened_previous_page, 'The find toolbar is present on the previous page')

        # Navigate forward to the page
        click(arrow_forward_button_pattern)
        find_toolbar_is_opened_next_page = exists(wiki_logo, 10)

        assert_true(self, find_toolbar_is_opened_next_page, 'The find toolbar is present on the next page')

