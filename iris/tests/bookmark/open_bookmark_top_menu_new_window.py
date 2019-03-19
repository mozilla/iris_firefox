# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a bookmark in a New Window using contextual menu ' \
                    'from \'Other Bookmarks\' section from Bookmarks menu'
        self.test_case_id = '163210'
        self.test_suite_id = '2525'
        self.locale = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        firefox_bookmark_top_menu_pattern = Pattern('firefox_bookmark_top_menu.png')
        open_bookmark_new_window_pattern = Pattern('open_bookmark_in_new_window.png')
        other_bookmarks_pattern = Pattern('other_bookmarks.png')

        open_firefox_menu()

        top_menu_located = exists(bookmarks_top_menu_pattern)
        assert_true(self, top_menu_located, 'Firefox menu is located')

        click(bookmarks_top_menu_pattern)

        bookmarks_dropdown_opened = exists(other_bookmarks_pattern)
        assert_true(self, bookmarks_dropdown_opened, 'Bookmarks dropdown firefox menu is opened')

        other_bookmarks_location = find(other_bookmarks_pattern)

        click(other_bookmarks_pattern)

        firefox_bookmark_top_menu_located = exists(firefox_bookmark_top_menu_pattern)
        assert_true(self, firefox_bookmark_top_menu_located, 'Bookmarks are displayed in top menu')

        firefox_bookmark_item_location = find(firefox_bookmark_top_menu_pattern)    # Required to guarantee bookmarks
                                                                                    # list will not disappear
        hover(Location(SCREEN_WIDTH, other_bookmarks_location.y))

        hover(Location(SCREEN_WIDTH, firefox_bookmark_item_location.y))

        right_click(firefox_bookmark_top_menu_pattern)

        context_menu_opened = exists(open_bookmark_new_window_pattern)
        assert_true(self, context_menu_opened, 'Bookmark context menu is opened')

        click(open_bookmark_new_window_pattern)

        webpage_opened = exists(LocalWeb.FIREFOX_LOGO)
        assert_true(self, webpage_opened, 'Expected webpage is properly displayed')

        close_window()
