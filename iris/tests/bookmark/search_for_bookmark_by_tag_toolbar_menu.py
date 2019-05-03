# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search for available bookmarks from Bookmarks Toolbar menu by tag.'
        self.test_case_id = '166039'
        self.test_suite_id = '2525'
        self.locales = ['en-US']
        self.exclude = [Platform.MAC]
        self.blocked_by = {'id': '1527258', 'platform': Platform.WINDOWS}

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        search_bookmarks_option_pattern = LibraryMenu.BookmarksOption.SEARCH_BOOKMARKS
        toolbar_bookmarks_top_menu_item_pattern = Pattern('bookmarks_toolbar_menu_option.png')
        getting_started_bookmark_top_menu_pattern = Pattern('getting_started_top_menu.png')
        focused_url_bar_with_asterisk_pattern = Pattern('focused_search_field.png')
        search_by_tag_result_pattern = Pattern('tagged_bookmark_search_result.png')
        bookmarks_menu_item_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        properties_option_pattern = Pattern('bookmark_properties_button.png')
        save_button_pattern = Pattern('save_bookmark_name.png')

        open_firefox_menu()

        bookmark_menu_item_available = exists(bookmarks_menu_item_top_menu_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, bookmark_menu_item_available, '\'Bookmarks\' option is available on Firefox top menu')

        click(bookmarks_menu_item_top_menu_pattern)

        toolbar_bookmarks_available_on_top_menu = exists(toolbar_bookmarks_top_menu_item_pattern,
                                                         Settings.FIREFOX_TIMEOUT)
        assert_true(self, toolbar_bookmarks_available_on_top_menu,
                    '\'Bookmarks Toolbar\' option available in \'Bookmarks\' section from top menu')

        mouse_move(toolbar_bookmarks_top_menu_item_pattern)

        getting_started_bookmark_available = exists(getting_started_bookmark_top_menu_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, getting_started_bookmark_available,
                    '\'Getting started\' bookmark available in \'Bookmarks\' section from top menu')

        right_click(getting_started_bookmark_top_menu_pattern)

        properties_option_appeared = exists(properties_option_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, properties_option_appeared, '\'Properties\' option available after right-click at bookmark')

        click(properties_option_pattern)

        tags_field_available = exists(Bookmarks.StarDialog.TAGS_FIELD, Settings.FIREFOX_TIMEOUT)
        assert_true(self, tags_field_available, '\'Tags\' field available in \'Properties\' window')

        click(Bookmarks.StarDialog.TAGS_FIELD)

        paste('test')

        click(save_button_pattern)

        try:
            properties_window_closed = wait_vanish(save_button_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
            assert_true(self, properties_window_closed,
                        '\'Properties\' window for \'Getting started\' bookmark closed')
        except FindError:
            raise FindError('\'Properties\' window for \'Getting started\' bookmark didn\'t close')

        library_menu_available = exists(NavBar.LIBRARY_MENU, Settings.FIREFOX_TIMEOUT)
        assert_true(self, library_menu_available, '\'Library menu\' button is available')

        click(NavBar.LIBRARY_MENU)

        library_menu_displayed = exists(LibraryMenu.BOOKMARKS_OPTION, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, library_menu_displayed,
                    '\'Bookmark option\' available in \'View history, saved '
                    'bookmarks and more\' menu section is correctly displayed.')

        click(LibraryMenu.BOOKMARKS_OPTION)

        search_bookmarks_option_available = exists(search_bookmarks_option_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, search_bookmarks_option_available,
                    'Bookmarks menu is displayed and \'Search bookmarks\' '
                    'option from \'Bookmarks\' toolbar menu available.')

        click(search_bookmarks_option_pattern)

        try:
            menu_closed = wait_vanish(search_bookmarks_option_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
            assert_true(self, menu_closed, 'The \'Bookmarks toolbar menu\' is dismissed.')
        except FindError:
            raise FindError('The \'Bookmarks toolbar menu\' didn\'t dismiss.')

        url_bar_focused = exists(focused_url_bar_with_asterisk_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, url_bar_focused, 'The focus is in the URL address bar after a \'*\'.')

        click(focused_url_bar_with_asterisk_pattern)

        paste('test')

        bookmark_found_by_tag = exists(search_by_tag_result_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, bookmark_found_by_tag,
                    'All the valid results are displayed under the URL bar with a star-shaped button in front.')
