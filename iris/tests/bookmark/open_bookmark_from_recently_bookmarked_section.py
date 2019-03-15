# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a bookmark from the Recently Bookmarked section'
        self.test_case_id = '165484'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        library_button_exists = exists(NavBar.LIBRARY_MENU, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, library_button_exists, 'View history, saved bookmarks and more section exists')

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_menu_option_exists, 'The Bookmarks menu is correctly displayed')

        click(LibraryMenu.BOOKMARKS_OPTION)

        recently_firefox_bookmark_exists = exists(LocalWeb.FIREFOX_BOOKMARK, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, recently_firefox_bookmark_exists, 'Firefox bookmark exists in recently bookmarked section')

        click(LocalWeb.FIREFOX_BOOKMARK)

        firefox_full_logo_exists = exists(LocalWeb.FIREFOX_IMAGE, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, firefox_full_logo_exists, 'Bookmark is correctly opened in the current tab.')

        bookmark_opened_in_current_tab = exists(LocalWeb.IRIS_LOGO_INACTIVE_TAB, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_false(self, bookmark_opened_in_current_tab,
                     'The page that was previously displayed in the current tab is no longer displayed')
