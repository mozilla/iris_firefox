# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Add a New Bookmark from Bookmarks Sidebar'
        self.test_case_id = '168930'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        new_bookmark_option_pattern = Library.Organize.NEW_BOOKMARK
        new_bookmark_created_pattern = Pattern('new_bookmark_created.png')

        if not Settings.is_mac():
            bookmarks_menu_pattern = Library.BOOKMARKS_MENU
        else:
            bookmarks_menu_pattern = Pattern('bookmark_menu_section.png')

        if Settings.is_windows():
            new_bookmark_panel_pattern = Bookmarks.StarDialog.NEW_BOOKMARK
        else:
            new_bookmark_panel_pattern = Pattern('new_bookmark_panel.png')

        bookmarks_sidebar('open')

        bookmarks_sidebar_menu_exists = exists(SidebarBookmarks.BOOKMARKS_HEADER, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_sidebar_menu_exists, 'Bookmarks Sidebar is correctly displayed.')

        bookmarks_menu_exists = exists(bookmarks_menu_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_menu_exists, 'Bookmarks menu section exists')

        right_click(bookmarks_menu_pattern)

        new_bookmark_option_exists = exists(new_bookmark_option_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, new_bookmark_option_exists, 'New Bookmark option exists')

        click(new_bookmark_option_pattern)

        new_bookmark_panel_exists = exists(new_bookmark_panel_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, new_bookmark_panel_exists, 'A New Bookmark... window is opened.')

        type(Key.TAB)
        paste('google.com')

        type(Key.TAB)
        paste('search, media')

        if not Settings.is_mac():
            [type(Key.TAB) for _ in range(2)]
        else:
            type(Key.TAB)

        paste('search')

        type(Key.ENTER)

        click(bookmarks_menu_pattern)

        new_bookmark_created_exists = exists(new_bookmark_created_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, new_bookmark_created_exists, 'The new bookmark is added in the selected section.')
