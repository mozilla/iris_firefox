# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open a bookmark from \'Other Bookmarks\' section from Bookmarks menu',
        locale=['en-US'],
        test_case_id='163207',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        other_bookmarks_pattern = Pattern('other_bookmarks.png')
        firefox_bookmark_top_menu_pattern = Pattern('firefox_bookmark_top_menu.png').similar(0.9)

        open_firefox_menu()

        top_menu_displayed = exists(bookmarks_top_menu_pattern)
        assert top_menu_displayed is True, 'Top menu is displayed'

        click(bookmarks_top_menu_pattern)

        dropdown_displayed = exists(other_bookmarks_pattern)
        assert dropdown_displayed is True, 'Bookmark dropdown menu is displayed'

        other_bookmarks_item_location = find(other_bookmarks_pattern)

        click(other_bookmarks_pattern)

        bookmark_found = exists(firefox_bookmark_top_menu_pattern)
        assert bookmark_found is True, 'Needed bookmark is located in other bookmarks'

        firefox_bookmark_location = find(firefox_bookmark_top_menu_pattern)

        # Required to guarantee bookmarks list will not disappear
        hover(Location(Screen.SCREEN_WIDTH, other_bookmarks_item_location.y))
        hover(Location(Screen.SCREEN_WIDTH, firefox_bookmark_location.y))

        click(firefox_bookmark_top_menu_pattern)

        webpage_loaded = exists(LocalWeb.FIREFOX_LOGO)
        assert webpage_loaded is True, 'Needed webpage is loaded'

        previous_tab_not_displayed = not exists(LocalWeb.IRIS_LOGO_INACTIVE_TAB)
        assert previous_tab_not_displayed is True, 'Webpage was opened in current tab'
