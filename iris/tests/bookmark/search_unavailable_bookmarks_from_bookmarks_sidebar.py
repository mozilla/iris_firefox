# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search for unavailable bookmarks from Bookmarks Sidebar'
        self.test_case_id = '168921'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        Override the setup method to use a pre-canned bookmarks profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        bookmarks_sidebar_website_logo_pattern = Pattern('bookmarks_sidebar_logo.png')
        bookmarks_sidebar_menu_header_pattern = SidebarBookmarks.BOOKMARKS_HEADER

        bookmarks_sidebar('open')

        bookmarks_sidebar_menu_exists = exists(bookmarks_sidebar_menu_header_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarks_sidebar_menu_exists, 'Bookmarks Sidebar is correctly displayed.')

        type('SoundCloud')

        bookmarks_sidebar_logo_exists = exists(bookmarks_sidebar_website_logo_pattern, DEFAULT_UI_DELAY_LONG)
        assert_false(self, bookmarks_sidebar_logo_exists, 'Nothing is displayed in the Bookmarks Sidebar.')
