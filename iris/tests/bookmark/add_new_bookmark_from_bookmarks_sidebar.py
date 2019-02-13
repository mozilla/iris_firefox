# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Add a New Bookmark from Bookmarks Sidebar '
        self.test_case_id = '168930'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        bookmarks_sidebar_menu_header_pattern = SidebarBookmarks.BOOKMARKS_HEADER
        new_bookmark_option_pattern = Library.Organize.NEW_BOOKMARK
        new_bookmark_panel_pattern = Bookmarks.StarDialog.NEW_BOOKMARK
        bookmarks_menu_pattern = Library.BOOKMARKS_MENU
        new_bookmark_created_pattern = Pattern('new_bookmark_created.png')

        bookmarks_sidebar('open')

        bookmarks_sidebar_menu_exists = exists(bookmarks_sidebar_menu_header_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarks_sidebar_menu_exists, 'Bookmarks Sidebar is correctly displayed.')

        bookmarks_menu_exists = exists(bookmarks_menu_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarks_menu_exists, 'Bookmarks menu section exists')
        right_click(bookmarks_menu_pattern)

        new_bookmark_option_exists = exists(new_bookmark_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, new_bookmark_option_exists, 'New Bookmark option exists')
        click(new_bookmark_option_pattern)

        new_bookmark_panel_exists = exists(new_bookmark_panel_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, new_bookmark_panel_exists, 'A New Bookmark... window is opened.')

        type(Key.TAB)
        paste('google.com')

        type(Key.TAB)
        paste('search, media')

        [type(Key.TAB) for _ in range(2)]
        paste('search')

        type(Key.ENTER)

        click(bookmarks_menu_pattern)

        new_bookmark_created_exists = exists(new_bookmark_created_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, new_bookmark_created_exists, 'The new bookmark is added in the selected section.')







