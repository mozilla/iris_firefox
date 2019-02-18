# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Add a new bookmarks separator from Bookmarks Sidebar'
        self.test_case_id = '168932'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        separator_line_pattern = Pattern('separator.png')
        bookmark_site_pattern = Pattern('bookmark_site.png')
        mozilla_bookmark_pattern = Pattern('mozilla_bookmark.png')
        new_separator_pattern = Library.Organize.NEW_SEPARATOR

        if not Settings.is_mac():
            bookmark_menu_pattern = Library.BOOKMARKS_MENU
        else:
            bookmark_menu_pattern = Pattern('bookmarks_menu.png')

        bookmarks_sidebar('open')

        bookmark_menu_exists = exists(bookmark_menu_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_menu_exists, 'Bookmarks Sidebar is correctly displayed')

        click(bookmark_menu_pattern)

        mozilla_bookmark_exists = exists(mozilla_bookmark_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, mozilla_bookmark_exists, 'Mozilla bookmarks button exists')

        click(mozilla_bookmark_pattern)

        bookmark_site_exists = exists(bookmark_site_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_site_exists, 'Website bookmark exists')

        right_click(bookmark_site_pattern)

        new_separator_exists = exists(new_separator_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, new_separator_exists, 'Separator button exists')

        click(new_separator_pattern)

        separator_line_exists = exists(separator_line_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, separator_line_exists, 'A new separator is displayed above the selected bookmark.')
