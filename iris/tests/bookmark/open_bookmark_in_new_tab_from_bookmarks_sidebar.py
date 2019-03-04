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
        open_in_new_tab_option_pattern = Pattern('open_in_new_tab.png')
        firefox_sidebar_logo_pattern = Pattern('firefox_bookmark.png')
        iris_tab_pattern = Pattern('iris_tab.png')

        if Settings.is_mac():
            other_bookmarks_pattern = Pattern('other_bookmarks.png')
        else:
            other_bookmarks_pattern = Library.OTHER_BOOKMARKS

        bookmarks_sidebar('open')

        bookmarks_sidebar_menu_exists = exists(SidebarBookmarks.BOOKMARKS_HEADER, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_sidebar_menu_exists, '\'Bookmarks Sidebar\' is correctly displayed.')

        other_bookmarks_exists = exists(other_bookmarks_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, other_bookmarks_exists, '\'Other bookmarks\' folder exists on the sidebar.')

        click(other_bookmarks_pattern)

        firefox_sidebar_logo_exists = exists(firefox_sidebar_logo_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_sidebar_logo_exists, '\'Firefox\' bookmark exists in the \'Other bookmarks\' folder')

        right_click(firefox_sidebar_logo_pattern)

        open_option_exists = exists(open_in_new_tab_option_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, open_option_exists,
                    '\'Open in new tab\' option is displayed after right-click at the Firefox bookmark icon')

        click(open_in_new_tab_option_pattern)

        select_tab(2)
        firefox_full_logo_exists = exists(LocalWeb.FIREFOX_IMAGE, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, firefox_full_logo_exists, 'The web page is opened in the new tab')

        select_tab(1)
        iris_tab_available = exists(iris_tab_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, iris_tab_available, 'Initial tab exists after opening bookmarked page in new tab')

