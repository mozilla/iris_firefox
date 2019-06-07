# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open the Library from the Bookmarks menu',
        locale=['en-US'],
        test_case_id='165493',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        show_all_bookmarks_button_pattern = Pattern('show_all_bookmarks_button.png')

        library_button_exists = exists(NavBar.LIBRARY_MENU)
        assert library_button_exists, 'View history, saved bookmarks and more section exists'

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION)
        assert bookmarks_menu_option_exists is True, 'The Bookmarks option exists'

        click(LibraryMenu.BOOKMARKS_OPTION)

        show_all_bookmarks_button_exists = exists(show_all_bookmarks_button_pattern)
        assert show_all_bookmarks_button_exists is True, 'The Bookmarks menu is correctly displayed'

        click(show_all_bookmarks_button_pattern)

        library_exists = exists(Library.TITLE)
        assert library_exists is True, 'The Library is opened'

        click(Library.TITLE)

        close_window_control('auxiliary')
