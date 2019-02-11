# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a bookmark using \'Open\' option from the contextual menu'
        self.test_case_id = '168926'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup
        Override the setup method to use a pre-canned bookmarks profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        wikipedia_sidebar_logo_pattern = Pattern('wiki_logo.png')
        open_in_new_tab_option_pattern = Pattern('open_in_new_tab.png')
        new_tab_is_opened_pattern = Pattern('new_tab_opened.png').similar(0.95)
        bookmarks_sidebar_menu_header_pattern = SidebarBookmarks.BOOKMARKS_HEADER
        if Settings.is_mac():
            other_bookmarks_pattern = Pattern('other_bookmarks.png')
        else:
            other_bookmarks_pattern = Library.OTHER_BOOKMARKS

        bookmarks_sidebar('open')

        bookmarks_sidebar_menu_exists = exists(bookmarks_sidebar_menu_header_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarks_sidebar_menu_exists, 'Bookmarks Sidebar is correctly displayed.')

        other_bookmarks_exists = exists(other_bookmarks_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, other_bookmarks_exists, 'Other bookmarks exists')
        click(other_bookmarks_pattern)

        wikipedia_sidebar_logo_exists = exists(wikipedia_sidebar_logo_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, wikipedia_sidebar_logo_exists, 'Wikipedia bookmark exists')
        right_click(wikipedia_sidebar_logo_pattern)

        open_option_exists = exists(open_in_new_tab_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, open_option_exists, 'Open option exists')
        click(open_in_new_tab_option_pattern)

        new_tab_is_opened_not_exists = exists(new_tab_is_opened_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, new_tab_is_opened_not_exists, 'The web page is opened at the new tab')

