# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Empty "Other Bookmarks" section from Bookmarks menu'
        self.test_suite_id = '2525'
        self.test_case_id = '163206'
        self.locale = ['en-US']

    def run(self):
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        empty_folder_stub_pattern = Pattern('empty_folder.png')
        other_bookmarks_item_pattern = Pattern('other_bookmarks.png')

        open_firefox_menu()

        top_menu_displayed = exists(bookmarks_top_menu_pattern)
        assert_true(self, top_menu_displayed, 'Firefox menu is properly displayed')

        click(bookmarks_top_menu_pattern)

        bookmarks_dropdown_displayed = exists(other_bookmarks_item_pattern)
        assert_true(self, bookmarks_dropdown_displayed, 'Bookmarks menu is properly displayed')

        click(other_bookmarks_item_pattern)

        no_other_bookmarks = exists(empty_folder_stub_pattern)
        assert_true(self, no_other_bookmarks, '"Other Bookmarks" section is empty')

        click(NavBar.HAMBURGER_MENU)

        restore_firefox_focus()
