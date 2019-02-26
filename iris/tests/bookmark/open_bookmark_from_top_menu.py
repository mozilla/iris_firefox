# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a bookmark from \'Other Bookmarks\' section from Bookmarks menu'
        self.test_suite_id = '2525'
        self.test_case_id = '163207'
        self.locale = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        other_bookmarks_pattern = Pattern('other_bookmarks.png')
        firefox_bookmark_top_menu_pattern = Pattern('firefox_bookmark_top_menu.png').similar(0.95)

        open_firefox_menu()

        top_menu_displayed = exists(bookmarks_top_menu_pattern)
        assert_true(self, top_menu_displayed, 'Top menu is displayed')

        click(bookmarks_top_menu_pattern)
        dropdown_displayed = exists(other_bookmarks_pattern)
        assert_true(self, dropdown_displayed, 'Bookmark dropdown menu is displayed')

        click(other_bookmarks_pattern)
        bookmark_found = exists(firefox_bookmark_top_menu_pattern)
        assert_true(self, bookmark_found, 'Needed bookmark is located in other bookmarks')

        type(Key.RIGHT)

        click(firefox_bookmark_top_menu_pattern)
        webpage_loaded = exists(LocalWeb.FIREFOX_LOGO)
        assert_true(self, webpage_loaded, 'Needed webpage is loaded')
