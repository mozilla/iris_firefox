# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Search for unavailable bookmarks from Bookmarks Toolbar menu',
        locale=['en-US'],
        test_case_id='165482',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        library_button_pattern = NavBar.LIBRARY_MENU
        bookmarks_menu_option_pattern = LibraryMenu.BOOKMARKS_OPTION
        search_bookmarks_pattern = LibraryMenu.BookmarksOption.SEARCH_BOOKMARKS
        focused_search_field_pattern = Pattern('focused_search_field.png')
        bookmarked_site_icon_under_url_pattern = Pattern('bookmarked_site_icon.png').similar(0.9)
        search_with_default_engine_pattern = Pattern('search_with_default_engine.png')

        library_button_exists = exists(library_button_pattern)
        assert library_button_exists is True, 'View history, saved bookmarks and more section exists'

        click(library_button_pattern)

        bookmarks_menu_option_exists = exists(bookmarks_menu_option_pattern)
        assert bookmarks_menu_option_exists is True, 'Bookmarks menu option exists'

        click(bookmarks_menu_option_pattern)

        search_bookmarks_exists = exists(search_bookmarks_pattern)
        assert search_bookmarks_exists is True, 'Search Bookmarks button exists'

        click(search_bookmarks_pattern)

        try:
            bookmarking_menu_not_exists = wait_vanish(search_bookmarks_pattern)
            assert bookmarking_menu_not_exists is True, 'Bookmarks menu is dismissed'
        except FindError:
            raise FindError('Bookmarks menu is not dismissed')

        focused_search_field_exists = exists(focused_search_field_pattern)
        assert focused_search_field_exists is True, 'The focus is in the URL address bar after a \'* \'.'

        website_name = 'Telegram'

        paste(website_name)

        try:
            bookmarked_site_icon_under_url_not_exists = wait_vanish(bookmarked_site_icon_under_url_pattern)
            assert bookmarked_site_icon_under_url_not_exists is True, 'No bookmarks are displayed under the URL bar'
        except FindError:
            raise FindError('Bookmark exists under the URL bar')

        search_with_default_engine_exists = exists(search_with_default_engine_pattern)
        assert search_with_default_engine_exists is True, 'Telegram - Search with default search engine ' \
                                                          'is text is displayed'
