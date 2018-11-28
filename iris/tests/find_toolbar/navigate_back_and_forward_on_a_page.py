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
        wiki_logo = Pattern('wiki_logo_icon.png')
        new_tab_icon_pattern = Pattern('new_tab_icon.png')

        # Open Firefox and navigate to some popular websites on the same tab
        new_tab()
        test_page_local = self.get_asset_path('Wikipedia.htm')
        navigate(test_page_local)
        page_loaded = exists(wiki_logo, 20)
        assert_true(self, page_loaded, 'The website successfully loaded.')

        # Open the Find Toolbar
        open_find()
        edit_select_all()
        edit_delete()
        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, 15)
        assert_true(self, find_toolbar_is_opened, 'The find toolbar is opened')

        # Navigate back to the previous page (Click the left arrrow next to the URL bar)
        click(NavBar.BACK_BUTTON, 2)
        find_toolbar_is_opened_previous_page = exists(new_tab_icon_pattern, 10)
        assert_true(self, find_toolbar_is_opened_previous_page, 'The find toolbar is present on the previous page')

        # Navigate forward to the next page (Click the right arrow next to the URL bar)
        click(NavBar.FORWARD_BUTTON)
        find_toolbar_is_opened_next_page = exists(wiki_logo, 10)
        assert_true(self, find_toolbar_is_opened_next_page, 'The find toolbar is present on the next page')

