# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Copy a bookmark from "Other Bookmarks" section - Bookmarks menu',
        locale=['en-US'],
        test_case_id='163216',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        bookmark_toolbar_top_menu_pattern = Pattern('bookmark_toolbar_top_menu.png')
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        copy_option_pattern = Pattern('copy_option.png')
        firefox_bookmark_top_menu_pattern = Pattern('firefox_bookmark_top_menu.png').similar(0.9)
        most_visited_bookmarks_pattern = Pattern('firefox_menu_most_visited_bookmarks.png')
        other_bookmarks_pattern = Pattern('other_bookmarks.png')
        paste_bookmark_pattern = Pattern('paste_bookmark.png')

        open_firefox_menu()

        firefox_menu_opened = exists(bookmarks_top_menu_pattern)
        assert firefox_menu_opened is True, 'Firefox menu is opened'

        click(bookmarks_top_menu_pattern)

        bookmarks_menu_displayed = exists(other_bookmarks_pattern)
        assert bookmarks_menu_displayed is True, 'Bookmarks menu is displayed'

        click(other_bookmarks_pattern)

        other_bookmarks_displayed = exists(firefox_bookmark_top_menu_pattern)
        assert other_bookmarks_displayed is True, '"Other bookmarks" section is displayed'

        other_bookmarks_location_y = find(other_bookmarks_pattern).y
        firefox_bookmark_item_y = find(firefox_bookmark_top_menu_pattern).y

        hover(Location(Screen.SCREEN_WIDTH, other_bookmarks_location_y))

        hover(Location(Screen.SCREEN_WIDTH, firefox_bookmark_item_y))

        right_click(firefox_bookmark_top_menu_pattern)

        bookmark_context_menu_displayed = exists(copy_option_pattern)
        assert bookmark_context_menu_displayed is True, 'Bookmark context menu is displayed'

        click(copy_option_pattern)

        bookmarks_menu_displayed = exists(bookmark_toolbar_top_menu_pattern)
        assert bookmarks_menu_displayed is True, 'Bookmarks menu is displayed'

        click(bookmark_toolbar_top_menu_pattern)

        most_visited_bookmarks_displayed = exists(most_visited_bookmarks_pattern)
        assert most_visited_bookmarks_displayed is True, '"Most visited bookmarks" item is displayed'

        right_click(most_visited_bookmarks_pattern)

        bookmark_context_menu_displayed = exists(paste_bookmark_pattern)
        assert bookmark_context_menu_displayed is True, 'Bookmark context menu is displayed'

        click(paste_bookmark_pattern)

        bookmark_pasted = exists(firefox_bookmark_top_menu_pattern)
        assert bookmark_pasted is True, 'Bookmark is pasted'

        bookmarks_menu_displayed = exists(other_bookmarks_pattern)
        assert bookmarks_menu_displayed is True, 'Bookmarks menu is displayed'

        click(other_bookmarks_pattern)

        bookmark_not_disappeared = exists(firefox_bookmark_top_menu_pattern)
        assert bookmark_not_disappeared is True, 'Bookmark didn\'t disappear'

        click(NavBar.HAMBURGER_MENU)

        restore_firefox_focus()
