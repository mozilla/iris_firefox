# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open a bookmark in a New Private Window using contextual ' \
                    'menu from \'Other Bookmarks\' section from Bookmarks menu',
        locale=['en-US'],
        test_case_id='163211',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        firefox_bookmark_top_menu_pattern = Pattern('firefox_bookmark_top_menu.png')
        open_bookmark_in_private_pattern = Pattern('open_bookmark_in_private.png')
        other_bookmarks_pattern = Pattern('other_bookmarks.png')

        open_firefox_menu()

        top_menu_located = exists(bookmarks_top_menu_pattern)
        assert top_menu_located is True, 'Firefox menu is opened'

        click(bookmarks_top_menu_pattern)

        bookmarks_dropdown_opened = exists(other_bookmarks_pattern)
        assert bookmarks_dropdown_opened is True, 'Bookmarks menu is opened'

        other_bookmarks_location = find(other_bookmarks_pattern)

        click(other_bookmarks_pattern)

        firefox_bookmark_top_menu_located = exists(firefox_bookmark_top_menu_pattern)
        assert firefox_bookmark_top_menu_located is True, 'Bookmarks are displayed in top menu'

        # Required to guarantee bookmarks list will not disappear
        firefox_bookmark_item_location = find(firefox_bookmark_top_menu_pattern)
        hover(Location(Screen.SCREEN_WIDTH, other_bookmarks_location.y))
        hover(Location(Screen.SCREEN_WIDTH, firefox_bookmark_item_location.y))

        right_click(firefox_bookmark_top_menu_pattern)

        context_menu_opened = exists(open_bookmark_in_private_pattern)
        assert context_menu_opened is True, 'Bookmark context menu is opened'

        click(open_bookmark_in_private_pattern)

        webpage_opened = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert webpage_opened is True, 'Expected webpage is properly displayed'

        window_is_private = exists(PrivateWindow.private_window_pattern)
        assert window_is_private is True, 'Webpage is opened in private window'

        close_window()
