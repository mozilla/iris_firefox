# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Delete a bookmark from "Other Bookmarks" section - Bookmarks menu'
        self.test_case_id = '163218'
        self.test_suite_id = '2525'
        self.locale = ['en-US']
        self.exclude = [Platform.MAC]

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        delete_option_pattern = Pattern('delete_bookmark.png')
        firefox_bookmark_top_menu_pattern = Pattern('firefox_bookmark_top_menu.png').similar(0.9)
        other_bookmarks_pattern = Pattern('other_bookmarks.png')

        open_firefox_menu()

        firefox_menu_opened = exists(bookmarks_top_menu_pattern)
        assert_true(self, firefox_menu_opened, 'Firefox menu was opened')

        click(bookmarks_top_menu_pattern)

        bookmarks_menu_displayed = exists(other_bookmarks_pattern)
        assert_true(self, bookmarks_menu_displayed, 'Bookmarks menu is displayed')

        click(other_bookmarks_pattern)

        other_bookmarks_displayed = exists(firefox_bookmark_top_menu_pattern)
        assert_true(self, other_bookmarks_displayed, '"Other bookmarks" section is displayed')

        other_bookmarks_location_y = find(other_bookmarks_pattern).y
        firefox_bookmark_item_y = find(firefox_bookmark_top_menu_pattern).y

        hover(Location(SCREEN_WIDTH, other_bookmarks_location_y))

        hover(Location(SCREEN_WIDTH, firefox_bookmark_item_y))

        right_click(firefox_bookmark_top_menu_pattern)

        bookmark_context_menu_displayed = exists(delete_option_pattern)
        assert_true(self, bookmark_context_menu_displayed, 'Bookmark context menu is displayed')

        click(delete_option_pattern)

        bookmark_deleted = not exists(firefox_bookmark_top_menu_pattern)
        assert_true(self, bookmark_deleted, 'Bookmark is deleted')

        click(NavBar.HAMBURGER_MENU)

        restore_firefox_focus()
