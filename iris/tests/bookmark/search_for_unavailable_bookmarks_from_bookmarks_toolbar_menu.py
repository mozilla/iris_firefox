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
        bookmarked_site_icon_under_url_pattern = Pattern('bookmarked_site_icon.png').similar(0.9)

        NOT_BOOKMARKED_WEBSITE_NAME = 'Telegram'

        library_button_exists = exists(library_button_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, library_button_exists, 'View history, saved bookmarks and more section exists')

        click(library_button_pattern)

        bookmarks_menu_option_exists = exists(bookmarks_menu_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarks_menu_option_exists, 'Bookmarks menu option exists')

        click(bookmarks_menu_option_pattern)

        search_bookmarks_exists = exists(search_bookmarks_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, search_bookmarks_exists, 'Search Bookmarks button exists')

        click(search_bookmarks_pattern)

        try:
            bookmarking_menu_not_exists = wait_vanish(search_bookmarks_pattern, DEFAULT_UI_DELAY_LONG)
            assert_true(self, bookmarking_menu_not_exists, 'Bookmarks menu is dismissed')
        except FindError:
            raise FindError('Bookmarks menu is not dismissed')

        focused_search_field_exists = exists(focused_search_field_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, focused_search_field_exists, 'The focus is in the URL address bar after a \'* \'.')

        paste(NOT_BOOKMARKED_WEBSITE_NAME)

        try:
            bookmarked_site_icon_under_url_not_exists = wait_vanish(bookmarked_site_icon_under_url_pattern,
                                                                    DEFAULT_UI_DELAY_LONG)
            assert_true(self, bookmarked_site_icon_under_url_not_exists, 'No bookmarks are displayed under the URL bar')
        except FindError:
            raise FindError('Bookmark exists under the URL bar')

        search_with_default_engine_exists = exists(search_with_default_engine_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, search_with_default_engine_exists, 'Telegram - Search with default search engine '
                                                             'is text is displayed')
