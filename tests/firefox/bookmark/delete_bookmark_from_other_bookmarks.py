# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Delete a bookmark from "Other Bookmarks" section - Bookmarks menu',
        locale=['en-US'],
        test_case_id='163218',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        delete_option_pattern = Pattern('delete_bookmark.png')
        firefox_bookmark_top_menu_pattern = Pattern('firefox_bookmark_top_menu.png').similar(0.9)
        other_bookmarks_pattern = Pattern('other_bookmarks.png')

        open_firefox_menu()

        firefox_menu_opened = exists(bookmarks_top_menu_pattern)
        assert firefox_menu_opened is True, 'Firefox menu was opened'

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

        bookmark_context_menu_displayed = exists(delete_option_pattern)
        assert bookmark_context_menu_displayed is True, 'Bookmark context menu is displayed'

        click(delete_option_pattern)

        try:
            bookmark_deleted = wait_vanish(firefox_bookmark_top_menu_pattern)
            assert bookmark_deleted is True, 'Bookmark is deleted'
        except FindError:
            raise FindError('Bookmark is not deleted')

        type(Key.ESC)
        type(Key.ESC)

        restore_firefox_focus()
