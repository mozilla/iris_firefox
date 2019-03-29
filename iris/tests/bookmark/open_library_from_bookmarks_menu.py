# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open the Library from the Bookmarks menu'
        self.test_case_id = '165493'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        show_all_bookmarks_button_pattern = Pattern('show_all_bookmarks_button.png')

        library_button_exists = exists(NavBar.LIBRARY_MENU, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, library_button_exists, 'View history, saved bookmarks and more section exists')

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_menu_option_exists, 'The Bookmarks option exists')

        click(LibraryMenu.BOOKMARKS_OPTION)

        show_all_bookmarks_button_exists = exists(show_all_bookmarks_button_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, show_all_bookmarks_button_exists, 'The Bookmarks menu is correctly displayed')

        click(show_all_bookmarks_button_pattern)

        library_exists = exists(Library.TITLE, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, library_exists, 'The Library is opened')

        click(Library.TITLE)
        close_tab()
