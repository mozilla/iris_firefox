# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Empty "Other Bookmarks" section from Bookmarks menu',
        locale=['en-US'],
        test_case_id='163206',
        test_suite_id='2525'
    )
    def run(self, firefox):
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        empty_folder_stub_pattern = Pattern('empty_folder.png')
        other_bookmarks_item_pattern = Pattern('other_bookmarks.png')

        open_firefox_menu()

        top_menu_displayed = exists(bookmarks_top_menu_pattern)
        assert top_menu_displayed is True, 'Firefox menu is properly displayed'

        click(bookmarks_top_menu_pattern)

        bookmarks_dropdown_displayed = exists(other_bookmarks_item_pattern)
        assert bookmarks_dropdown_displayed is True, 'Bookmarks menu is properly displayed'

        click(other_bookmarks_item_pattern)

        no_other_bookmarks = exists(empty_folder_stub_pattern)
        assert no_other_bookmarks is True, '"Other Bookmarks" section is empty'

        click(NavBar.HAMBURGER_MENU)

        restore_firefox_focus()
