# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bookmarks menu from the Toolbar menu'
        self.test_case_id = '165472'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        bookmarks_title_pattern = Pattern('bookmarks_title.png')
        bookmark_this_page_pattern = Pattern('bookmark_this_page.png')
        show_all_bookmarks_pattern = Pattern('show_all_bookmarks_button.png')
        recently_bookmarked_label_pattern = Pattern('recently_bookmarked_label.png')

        library_button_exists = exists(NavBar.LIBRARY_MENU, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, library_button_exists, 'View history, saved bookmarks and more section exists')

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_menu_option_exists, 'The Bookmarks menu is correctly displayed')

        click(LibraryMenu.BOOKMARKS_OPTION)

        back_button_exists = exists(Utils.LIBRARY_BACK_BUTTON, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, back_button_exists, 'Back button is displayed')

        bookmarks_title_exists = exists(bookmarks_title_pattern)
        assert_true(self, bookmarks_title_exists, 'Bookmarks title is displayed')

        bookmark_this_page_exists = exists(bookmark_this_page_pattern)
        assert_true(self, bookmark_this_page_exists, 'Bookmark this page button is displayed')

        bookmarking_tools_exists = exists(LibraryMenu.BookmarksOption.BOOKMARKING_TOOLS)
        assert_true(self, bookmarking_tools_exists, 'Bookmarking Tools button is displayed')

        search_bookmarks_exists = exists(LibraryMenu.BookmarksOption.SEARCH_BOOKMARKS)
        assert_true(self, search_bookmarks_exists, 'Search Bookmarks button is displayed')

        recently_bookmarked_label_exists = exists(recently_bookmarked_label_pattern)
        assert_true(self, recently_bookmarked_label_exists, 'Recently bookmarked section is displayed')

        show_all_bookmarks_exists = exists(show_all_bookmarks_pattern)
        assert_true(self, show_all_bookmarks_exists, 'Show all bookmarks button is displayed')
