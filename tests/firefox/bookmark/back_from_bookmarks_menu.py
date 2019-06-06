# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Back from the Bookmarks menu',
        locale=['en-US'],
        test_case_id='165473',
        test_suite_id='2525'
    )
    def run(self, firefox):
        library_icon_pattern = NavBar.LIBRARY_MENU
        bookmarks_option_pattern = LibraryMenu.BOOKMARKS_OPTION
        library_back_button_pattern = Utils.LIBRARY_BACK_BUTTON
        bookmarking_tools_pattern = LibraryMenu.BookmarksOption.BOOKMARKING_TOOLS

        library_icon_exists = exists(library_icon_pattern)
        assert library_icon_exists is True, ' View history, saved bookmarks and more section button exists'

        click(library_icon_pattern)

        bookmarks_option_exists = exists(bookmarks_option_pattern)
        assert bookmarks_option_exists is True, 'The Bookmarks option exists'

        click(bookmarks_option_pattern)

        bookmark_menu_exists = exists(bookmarking_tools_pattern)
        assert bookmark_menu_exists is True, 'The Bookmarks menu is correctly displayed.'

        library_back_button_exists = exists(library_back_button_pattern)
        assert library_back_button_exists is True, 'Button back exists'

        click(library_back_button_pattern)

        menu_exists = exists(bookmarks_option_pattern)
        assert menu_exists is True, 'View history, saved bookmarks and more section is displayed.'





