# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='[Win/Linux] Paste a bookmark in \'Other Bookmarks\' section from Bookmarks menu',
        locale=['en-US'],
        test_case_id='163217',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        bookmark_toolbar_top_menu_pattern = Pattern('bookmark_toolbar_top_menu.png')
        cut_option_pattern = Pattern('cut_option.png')
        firefox_bookmark_top_menu_pattern = Pattern('firefox_bookmark_top_menu.png').similar(0.9)
        getting_started_pattern = Pattern('getting_started_top_menu.png')
        other_bookmarks_pattern = Pattern('other_bookmarks.png')
        paste_option_pattern = Pattern('paste_option.png')
        click_timeout = 1

        open_firefox_menu()

        firefox_menu_opened = exists(bookmarks_top_menu_pattern)
        assert firefox_menu_opened is True, 'Firefox menu is opened'

        click(bookmarks_top_menu_pattern)

        bookmarks_menu_opened = exists(bookmark_toolbar_top_menu_pattern)
        assert bookmarks_menu_opened is True, 'Bookmarks menu is opened'

        click(bookmark_toolbar_top_menu_pattern)

        bookmarks_content_displayed = exists(getting_started_pattern)
        assert bookmarks_content_displayed is True, '"Bookmarks toolbar" folder content is displayed'

        bookmark_toolbar_top_menu_location = find(bookmark_toolbar_top_menu_pattern)
        getting_started_bookmark_location = find(getting_started_pattern)
        loop_location = Location(Screen.SCREEN_WIDTH, bookmark_toolbar_top_menu_location.y)

        hover(loop_location, click_timeout)

        loop_location.y = getting_started_bookmark_location.y

        hover(loop_location, click_timeout)

        right_click(getting_started_pattern)

        context_menu_cut_displayed = exists(cut_option_pattern)
        assert context_menu_cut_displayed is True, 'Context menu "Cut" option is displayed'

        click(cut_option_pattern)

        bookmarks_menu_still_displayed = exists(other_bookmarks_pattern)
        assert bookmarks_menu_still_displayed is True, 'Bookmarks menu still displayed after bookmark was cut'

        click(other_bookmarks_pattern)

        other_bookmarks_displayed = exists(firefox_bookmark_top_menu_pattern)
        assert other_bookmarks_displayed is True, '"Other bookmarks" folder content is displayed'

        other_bookmarks_location = find(bookmark_toolbar_top_menu_pattern)
        firefox_bookmark_location = find(firefox_bookmark_top_menu_pattern)
        loop_location = Location(Screen.SCREEN_WIDTH, other_bookmarks_location.y)

        hover(loop_location, click_timeout)

        loop_location.y = firefox_bookmark_location.y

        hover(loop_location, click_timeout)

        right_click(firefox_bookmark_top_menu_pattern)

        context_menu_paste_displayed = exists(paste_option_pattern)
        assert context_menu_paste_displayed is True, 'Context menu "Paste" option is displayed'

        click(paste_option_pattern)

        bookmark_pasted = exists(getting_started_pattern)
        assert bookmark_pasted is True, 'Expected bookmark was pasted into "Other bookmarks" folder'

        click(NavBar.HAMBURGER_MENU)

        restore_firefox_focus()
