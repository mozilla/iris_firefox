# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a bookmark using contextual menu from \'Other Bookmarks\' section from Bookmarks menu'
        self.test_suite_id = '2525'
        self.test_case_id = '163208'
        self.locale = ['en-US']
        self.exclude = [Platform.MAC]

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        firefox_bookmark_top_menu_pattern = Pattern('firefox_bookmark_top_menu.png')
        open_bookmark_pattern = Pattern('open_bookmark_top_menu.png')
        other_bookmarks_pattern = Pattern('other_bookmarks.png')

        open_firefox_menu()

        top_menu_located = exists(bookmarks_top_menu_pattern)
        assert_true(self, top_menu_located, 'Firefox menu is located')

        click(bookmarks_top_menu_pattern)

        bookmarks_dropdown_opened = exists(other_bookmarks_pattern)
        assert_true(self, bookmarks_dropdown_opened, 'Bookmarks dropdown firefox menu is opened')

        other_bookmarks_item_location = find(other_bookmarks_pattern)

        click(other_bookmarks_pattern)

        firefox_bookmark_top_menu_located = exists(firefox_bookmark_top_menu_pattern)
        assert_true(self, firefox_bookmark_top_menu_located, 'Bookmarks are displayed in top menu')

        # Required to guarantee bookmarks list will not disappear
        firefox_bookmark_item_location = find(firefox_bookmark_top_menu_pattern)
        hover(Location(SCREEN_WIDTH, other_bookmarks_item_location.y))
        hover(Location(SCREEN_WIDTH, firefox_bookmark_item_location.y))

        right_click(firefox_bookmark_top_menu_pattern)

        context_menu_opened = exists(open_bookmark_pattern)
        assert_true(self, context_menu_opened, 'Bookmark context menu is opened')

        click(open_bookmark_pattern)

        webpage_opened = exists(LocalWeb.FIREFOX_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, webpage_opened, 'Bookmarked webpage is opened')

        webpage_opened_in_current_tab = not exists(LocalWeb.IRIS_LOGO_INACTIVE_TAB)
        assert_true(self, webpage_opened_in_current_tab, 'Bookmarked webpage was opened in current tab')
