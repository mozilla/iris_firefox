# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a bookmark in a New Tab from Bookmarks Sidebar'
        self.test_case_id = '168927'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        firefox_sidebar_logo_pattern = Pattern('firefox_bookmark.png')
        new_tab_is_opened_pattern = Pattern('new_tab_opened.png').similar(0.90)
        if Settings.is_mac():
            other_bookmarks_pattern = Pattern('other_bookmarks.png')
        else:
            other_bookmarks_pattern = Library.OTHER_BOOKMARKS
        if not Settings.is_linux():
            open_in_new_tab_option_pattern = Pattern('open_in_new_tab.png')

        bookmarks_sidebar('open')

        bookmarks_sidebar_menu_exists = exists(SidebarBookmarks.BOOKMARKS_HEADER, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarks_sidebar_menu_exists, 'Bookmarks Sidebar is correctly displayed.')

        other_bookmarks_exists = exists(other_bookmarks_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, other_bookmarks_exists, 'Other bookmarks exists')

        click(other_bookmarks_pattern)

        firefox_sidebar_logo_exists = exists(firefox_sidebar_logo_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, firefox_sidebar_logo_exists, 'Firefox bookmark exists')

        right_click(firefox_sidebar_logo_pattern)

        if not Settings.is_linux():
            open_option_exists = exists(open_in_new_tab_option_pattern, DEFAULT_FIREFOX_TIMEOUT)
            assert_true(self, open_option_exists, 'Open in new tab option exists')
            click(open_in_new_tab_option_pattern)
        else:
            firefox_sidebar_logo_exists = exists(firefox_sidebar_logo_pattern, DEFAULT_UI_DELAY_LONG)
            assert_false(self, firefox_sidebar_logo_exists, 'Open in new tab option exists')
            type('w')

        firefox_full_logo_exists = exists(LocalWeb.FIREFOX_IMAGE, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, firefox_full_logo_exists, 'Firefox content exists')

        new_tab_is_opened_not_exists = exists(new_tab_is_opened_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, new_tab_is_opened_not_exists, 'The web page is opened at the new tab')

