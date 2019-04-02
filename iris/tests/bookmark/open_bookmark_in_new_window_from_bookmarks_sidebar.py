# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a bookmark in a New Window from Bookmarks Sidebar'
        self.test_case_id = '168928'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        bookmarks_sidebar_menu_header_pattern = SidebarBookmarks.BOOKMARKS_HEADER
        firefox_sidebar_logo_pattern = Pattern('firefox_bookmark.png')
        open_in_new_window_option_pattern = Pattern('open_in_new_window.png')

        if Settings.is_mac():
            other_bookmarks_pattern = Pattern('other_bookmarks_from_sidebar.png')
        else:
            other_bookmarks_pattern = Library.OTHER_BOOKMARKS

        bookmarks_sidebar('open')

        bookmarks_sidebar_menu_exists = exists(bookmarks_sidebar_menu_header_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_sidebar_menu_exists, 'Bookmarks Sidebar is correctly displayed.')

        other_bookmarks_exists = exists(other_bookmarks_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, other_bookmarks_exists, 'Other bookmarks exists')

        click(other_bookmarks_pattern)

        firefox_sidebar_logo_exists = exists(firefox_sidebar_logo_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_sidebar_logo_exists, 'Firefox bookmark exists')

        right_click(firefox_sidebar_logo_pattern)

        open_option_exists = exists(open_in_new_window_option_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, open_option_exists, 'Open in New Window option exists')

        click(open_in_new_window_option_pattern)

        firefox_full_logo_exists = exists(LocalWeb.FIREFOX_IMAGE, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, firefox_full_logo_exists, 'Firefox content exists')

        close_window()

        iris_logo_exists = exists(LocalWeb.IRIS_LOGO, Settings.FIREFOX_TIMEOUT)
        assert_true(self, iris_logo_exists, 'The page is correctly opened in a new window.')
