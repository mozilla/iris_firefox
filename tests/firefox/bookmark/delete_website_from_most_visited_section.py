# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Delete a website from \'Most Visited\' section',
        locale=['en-US'],
        test_case_id='163204',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        firefox_menu_bookmarks_toolbar_pattern = Pattern('firefox_menu_bookmarks_toolbar.png')
        firefox_menu_most_visited_pattern = Pattern('firefox_menu_most_visited.png')
        firefox_pocket_bookmark_pattern = Pattern('pocket_most_visited.png')
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

        click(firefox_menu_most_visited_pattern)

        firefox_pocket_bookmark_exists = exists(firefox_pocket_bookmark_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert firefox_pocket_bookmark_exists is True, 'Most visited websites are displayed.'

        right_click(firefox_pocket_bookmark_pattern, 0)

        delete_option_exists = exists(delete_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert delete_option_exists is True, 'Delete option exists'

        click(delete_option_pattern)

        try:
            bookmark_deleted = wait_vanish(firefox_pocket_bookmark_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
            assert bookmark_deleted is True, 'The website is deleted from the list.'
        except FindError:
            raise FindError(' The website is not deleted from the list.')

        restore_firefox_focus()
