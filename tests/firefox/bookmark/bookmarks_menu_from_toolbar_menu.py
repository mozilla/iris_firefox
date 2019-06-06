# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmarks menu from the Toolbar menu',
        locale=['en-US'],
        test_case_id='165472',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        bookmarks_title_pattern = Pattern('bookmarks_title.png')
        bookmark_this_page_pattern = Pattern('bookmark_this_page.png')
        show_all_bookmarks_pattern = Pattern('show_all_bookmarks_button.png')
        recently_bookmarked_label_pattern = Pattern('recently_bookmarked_label.png')

        library_button_exists = exists(NavBar.LIBRARY_MENU, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert library_button_exists is True, 'View history, saved bookmarks and more section exists'

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_menu_option_exists is True, 'The Bookmarks menu is correctly displayed'

        click(LibraryMenu.BOOKMARKS_OPTION)

        back_button_exists = exists(Utils.LIBRARY_BACK_BUTTON, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert back_button_exists is True, 'Back button is displayed'

        bookmarks_title_exists = exists(bookmarks_title_pattern)
        assert bookmarks_title_exists is True, 'Bookmarks title is displayed'

        bookmark_this_page_exists = exists(bookmark_this_page_pattern)
        assert bookmark_this_page_exists is True, 'Bookmark this page button is displayed'

        bookmarking_tools_exists = exists(LibraryMenu.BookmarksOption.BOOKMARKING_TOOLS)
        assert bookmarking_tools_exists is True, 'Bookmarking Tools button is displayed'

        search_bookmarks_exists = exists(LibraryMenu.BookmarksOption.SEARCH_BOOKMARKS)
        assert search_bookmarks_exists is True, 'Search Bookmarks button is displayed'

        recently_bookmarked_label_exists = exists(recently_bookmarked_label_pattern)
        assert recently_bookmarked_label_exists is True, 'Recently bookmarked section is displayed'

        show_all_bookmarks_exists = exists(show_all_bookmarks_pattern)
        assert show_all_bookmarks_exists is True, 'Show all bookmarks button is displayed'
