# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Delete a bookmark from the Bookmarks Toolbar submenu',
        locale=['en-US'],
        test_case_id='163490',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        firefox_menu_bookmarks_toolbar_pattern = Pattern('firefox_menu_bookmarks_toolbar.png')
        firefox_menu_most_visited_pattern = Pattern('firefox_menu_most_visited.png')
        getting_started_pattern = Pattern('getting_started_top_menu.png')
        getting_started_toolbar_pattern = Pattern('getting_started_in_toolbar.png')
        delete_option_pattern = Pattern('delete_bookmark.png')

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert firefox_menu_bookmarks_exists is True, 'Firefox menu > Bookmarks exists'

        click(firefox_menu_bookmarks_pattern)

        bookmarks_toolbar_folder_exists = exists(firefox_menu_bookmarks_toolbar_pattern,
                                                 FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_toolbar_folder_exists is True, 'Firefox menu > Bookmarks > Bookmarks Toolbar folder exists'

        click(firefox_menu_bookmarks_toolbar_pattern)

        most_visited_folder_exists = exists(firefox_menu_most_visited_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert most_visited_folder_exists is True, 'Firefox menu > Bookmarks > Bookmarks Toolbar > Most Visited ' \
                                                   'folder exists'

        getting_started_exists = exists(getting_started_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert getting_started_exists is True, 'Firefox menu > Bookmarks > Bookmarks Toolbar > Getting Started ' \
                                               'bookmark exists'

        right_click(getting_started_pattern)

        delete_option_exists = exists(delete_option_pattern)
        assert delete_option_exists is True, 'Delete option exists'

        click(delete_option_pattern)

        try:
            getting_started_bookmark_removed = wait_vanish(getting_started_pattern)
            assert getting_started_bookmark_removed is True, 'Getting Started bookmark deleted from Firefox menu >' \
                                                             ' Bookmarks > Bookmarks Toolbar section'
        except FindError:
            raise FindError('Getting Started bookmark is not deleted')

        restore_firefox_focus()

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)

        open_bookmarks_toolbar()

        bookmark_removed_from_toolbar = exists(getting_started_toolbar_pattern)
        assert bookmark_removed_from_toolbar is False, 'The selected file is deleted from the **Bookmarks Toolbar**' \
                                                       ' section.'
