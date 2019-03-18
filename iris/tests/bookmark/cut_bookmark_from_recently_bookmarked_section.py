# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Cut a bookmark from the Recently Bookmarked section '
        self.test_case_id = '165489'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        cut_option_pattern = Pattern('cut_option.png')

        library_button_exists = exists(NavBar.LIBRARY_MENU, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, library_button_exists, 'View history, saved bookmarks and more section exists')

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_menu_option_exists, 'The Bookmarks menu is correctly displayed')

        click(LibraryMenu.BOOKMARKS_OPTION)

        recently_firefox_bookmark_exists = exists(LocalWeb.FIREFOX_BOOKMARK, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, recently_firefox_bookmark_exists, 'Firefox bookmark exists in recently bookmarked section')

        right_click(LocalWeb.FIREFOX_BOOKMARK)

        cut_option_exists = exists(cut_option_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, cut_option_exists, '\'Cut\' option exists')

        click(cut_option_pattern)





