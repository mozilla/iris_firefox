# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open a bookmarked website by drag&drop',
        locale=['en-US'],
        test_case_id='164168',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        most_visited_bookmarks_folder_pattern = Pattern('most_visited_top_menu_bookmarks_folder.png')
        bookmarks_top_menu_toolbar_menu_item_pattern = Pattern('firefox_menu_bookmarks_toolbar.png')
        bookmarks_top_menu_option = Pattern('firefox_menu_bookmarks.png')
        pocket_bookmark_pattern = Pattern('pocket_most_visited.png')

        open_firefox_menu()

        bookmarks_option_available_in_top_menu = exists(bookmarks_top_menu_option,
                                                        FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_option_available_in_top_menu is True, '\'Bookmarks\' menu item available in firefox top menu'

        click(bookmarks_top_menu_option)

        bookmarks_top_menu_toolbar_option_available = exists(bookmarks_top_menu_toolbar_menu_item_pattern)
        assert bookmarks_top_menu_toolbar_option_available is True, '\'Bookmarks toolbar\' option available ' \
                                                                    'in \'Bookmarks\' top menu section'

        click(bookmarks_top_menu_toolbar_menu_item_pattern)

        most_visited_bookmarks_folder_available = exists(most_visited_bookmarks_folder_pattern)
        assert most_visited_bookmarks_folder_available is True, '\'Most visited\' folder is available ' \
                                                                'on the bookmarks toolbar'

        most_visited_bookmarks_location = find(most_visited_bookmarks_folder_pattern)

        click(most_visited_bookmarks_folder_pattern)

        pocket_bookmark_available = exists(pocket_bookmark_pattern)
        assert pocket_bookmark_available, '\'Pocket\' bookmark is available in \'Most visited\' folder on ' \
                                          'the \'Bookmarks toolbar\' top menu section'

        pocket_bookmark_location = find(pocket_bookmark_pattern)

        # Required to guarantee bookmarks list will not disappear
        hover(Location(Screen.SCREEN_WIDTH, most_visited_bookmarks_location.y))
        hover(Location(Screen.SCREEN_WIDTH, pocket_bookmark_location.y))

        drag_drop(pocket_bookmark_pattern, Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2),
                  duration=FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        bookmark_opened = exists(LocalWeb.POCKET_IMAGE, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert bookmark_opened is True, 'The selected website is correctly opened.'
