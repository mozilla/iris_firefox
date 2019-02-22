# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search for unavailable bookmarks from Bookmarks Toolbar menu'
        self.test_case_id = '165482'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        library_button_pattern = NavBar.LIBRARY_MENU
        bookmarks_menu_option_pattern = LibraryMenu.BOOKMARKS_OPTION
        search_bookmarks_pattern = LibraryMenu.BookmarksOption.SEARCH_BOOKMARKS
        focused_search_field_pattern = Pattern('focused_search_field.png')
        search_with_default_engine_pattern = Pattern('search_with_default_engine.png')

        library_button_exists = exists(library_button_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, library_button_exists, 'View history, saved bookmarks and more section exists')

        click(library_button_pattern)

        bookmarks_menu_option_exists = exists(bookmarks_menu_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarks_menu_option_exists, 'Bookmarks menu option exists')

        click(bookmarks_menu_option_pattern)

        search_bookmarks_exists = exists(search_bookmarks_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, search_bookmarks_exists, 'Search Bookmarks button exists')

        click(search_bookmarks_pattern)

        focused_search_field_exists = exists(focused_search_field_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, focused_search_field_exists, ' the focus is in the URL address bar after a \'* \'.')

        bookmarks_menu_not_exists = exists(search_bookmarks_pattern, DEFAULT_UI_DELAY)
        assert_false(self, bookmarks_menu_not_exists, 'The menu is dismissed')

        type('Telegram')

        search_with_default_engine_exists = exists(search_with_default_engine_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, search_with_default_engine_exists, ' No bookmarks are displayed under the URL bar '
                                                             'and Telegram - Search with default search engine '
                                                             'is text is displayed')



