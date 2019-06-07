# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Search for available bookmarks from Bookmarks Toolbar menu by tag.',
        locale=['en-US'],
        test_case_id='166039',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC,
        blocked_by={'id': '1527258', 'platform': OSPlatform.WINDOWS}
    )
    def run(self, firefox):
        search_bookmarks_option_pattern = LibraryMenu.BookmarksOption.SEARCH_BOOKMARKS
        toolbar_bookmarks_top_menu_item_pattern = Pattern('bookmarks_toolbar_menu_option.png')
        getting_started_bookmark_top_menu_pattern = Pattern('getting_started_top_menu.png')
        focused_url_bar_with_asterisk_pattern = Pattern('focused_search_field.png')
        search_by_tag_result_pattern = Pattern('tagged_bookmark_search_result.png')
        bookmarks_menu_item_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        properties_option_pattern = Pattern('bookmark_properties_button.png')
        save_button_pattern = Pattern('save_bookmark_name.png')

        open_firefox_menu()

        bookmark_menu_item_available = exists(bookmarks_menu_item_top_menu_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_menu_item_available is True, '\'Bookmarks\' option is available on Firefox top menu'

        click(bookmarks_menu_item_top_menu_pattern)

        toolbar_bookmarks_available_on_top_menu = exists(toolbar_bookmarks_top_menu_item_pattern,
                                                         FirefoxSettings.FIREFOX_TIMEOUT)
        assert toolbar_bookmarks_available_on_top_menu is True, '\'Bookmarks Toolbar\' option available in ' \
                                                                '\'Bookmarks\' section from top menu'

        hover(toolbar_bookmarks_top_menu_item_pattern)

        getting_started_bookmark_available = exists(getting_started_bookmark_top_menu_pattern,
                                                    FirefoxSettings.FIREFOX_TIMEOUT)
        assert getting_started_bookmark_available is True, '\'Getting started\' bookmark available in' \
                                                           ' \'Bookmarks\' section from top menu'

        right_click(getting_started_bookmark_top_menu_pattern)

        properties_option_appeared = exists(properties_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert properties_option_appeared  is True, '\'Properties\' option available after right-click at bookmark'

        click(properties_option_pattern)

        tags_field_available = exists(Bookmarks.StarDialog.TAGS_FIELD, FirefoxSettings.FIREFOX_TIMEOUT)
        assert tags_field_available is True, '\'Tags\' field available in \'Properties\' window'

        click(Bookmarks.StarDialog.TAGS_FIELD)

        paste('test')

        click(save_button_pattern)

        try:
            properties_window_closed = wait_vanish(save_button_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
            assert properties_window_closed, '\'Properties\' window for \'Getting started\' bookmark closed'
        except FindError:
            raise FindError('\'Properties\' window for \'Getting started\' bookmark didn\'t close')

        library_menu_available = exists(NavBar.LIBRARY_MENU, FirefoxSettings.FIREFOX_TIMEOUT)
        assert library_menu_available  is True, '\'Library menu\' button is available'

        click(NavBar.LIBRARY_MENU)

        library_menu_displayed = exists(LibraryMenu.BOOKMARKS_OPTION, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert library_menu_displayed, '\'Bookmark option\' available in \'View history, saved bookmarks and more\' ' \
                                       'menu section is correctly displayed.'

        click(LibraryMenu.BOOKMARKS_OPTION)

        search_bookmarks_option_available = exists(search_bookmarks_option_pattern,
                                                   FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert search_bookmarks_option_available is True, 'Bookmarks menu is displayed and \'Search bookmarks\' ' \
                                                          'option from \'Bookmarks\' toolbar menu available.'

        click(search_bookmarks_option_pattern)

        try:
            menu_closed = wait_vanish(search_bookmarks_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
            assert menu_closed is True, 'The \'Bookmarks toolbar menu\' is dismissed.'
        except FindError:
            raise FindError('The \'Bookmarks toolbar menu\' didn\'t dismiss.')

        url_bar_focused = exists(focused_url_bar_with_asterisk_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert url_bar_focused is True, 'The focus is in the URL address bar after a \'*\'.'

        click(focused_url_bar_with_asterisk_pattern)

        paste('test')

        bookmark_found_by_tag = exists(search_by_tag_result_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_found_by_tag is True, 'All the valid results are displayed under the URL bar with a ' \
                                              'star-shaped button in front.'
