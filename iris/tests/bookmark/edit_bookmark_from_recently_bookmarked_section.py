# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Edit a bookmark from the Recently Bookmarked section '
        self.test_case_id = '165492'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        properties_option_pattern = Pattern('properties_option.png')
        properties_for_firefox_pattern = Pattern('properties_for_firefox.png')
        firefox_sidebar_logo_pattern = Pattern('firefox_bookmark.png')

        library_button_exists = exists(NavBar.LIBRARY_MENU, DEFAULT_UI_DELAY_LONG)
        assert_true(self, library_button_exists, 'View history, saved bookmarks and more section exists')

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarks_menu_option_exists, 'The Bookmarks menu is correctly displayed')

        click(LibraryMenu.BOOKMARKS_OPTION)

        firefox_sidebar_logo_exists = exists(firefox_sidebar_logo_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, firefox_sidebar_logo_exists, 'Firefox bookmarks exists')

        right_click(firefox_sidebar_logo_pattern)

        properties_option_exists = exists(properties_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, properties_option_exists, 'Properties option exists')

        click(properties_option_pattern)

        properties_for_firefox_exists = exists(properties_for_firefox_pattern)
        assert_true(self, properties_for_firefox_exists, '')