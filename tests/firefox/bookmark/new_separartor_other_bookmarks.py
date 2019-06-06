# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Add a new separator in "Other Bookmarks" section form Bookmarks menu',
        locale=['en-US'],
        test_case_id='163214',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        bookmarks_firefox_menu_pattern = Pattern('firefox_menu_bookmarks.png')
        firefox_bookmark_top_menu_pattern = Pattern('firefox_bookmark_top_menu.png')
        other_bookmarks_pattern = Pattern('other_bookmarks.png')
        new_separator_option_pattern = Pattern('new_separator_option.png')
        separator_in_front_bookmark_pattern = Pattern('separator_in_front_bookmark.png').similar(0.98)

        open_firefox_menu()

        firefox_menu_opened = exists(bookmarks_firefox_menu_pattern)
        assert firefox_menu_opened is True, 'Firefox menu is opened'

        click(bookmarks_firefox_menu_pattern)

        bookmarks_menu_opened = exists(other_bookmarks_pattern)
        assert bookmarks_menu_opened is True, 'Bookmarks menu is opened'

        click(other_bookmarks_pattern)

        other_bookmarks_displayed = exists(firefox_bookmark_top_menu_pattern)
        assert other_bookmarks_displayed is True, 'Other bookmarks list is displayed'

        other_bookmarks_location_y = find(other_bookmarks_pattern).y
        firefox_bookmark_item_y = find(firefox_bookmark_top_menu_pattern).y

        hover(Location(Screen.SCREEN_WIDTH, other_bookmarks_location_y))
        hover(Location(Screen.SCREEN_WIDTH, firefox_bookmark_item_y))

        right_click(firefox_bookmark_top_menu_pattern)

        context_menu_opened = exists(new_separator_option_pattern)
        assert context_menu_opened is True, 'Bookmark context menu is displayed'

        click(new_separator_option_pattern)

        separator_in_front_bookmark = exists(separator_in_front_bookmark_pattern)
        assert separator_in_front_bookmark is True, 'Separator is properly displayed in front of selected bookmark'

        click(NavBar.HAMBURGER_MENU)

        restore_firefox_focus()
