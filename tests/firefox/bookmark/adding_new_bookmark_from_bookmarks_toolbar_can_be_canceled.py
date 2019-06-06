# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Adding a new bookmark from the Bookmarks Toolbar can be canceled',
        locale=['en-US'],
        test_case_id='163813',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        firefox_menu_bookmarks_toolbar_pattern = Pattern('firefox_menu_bookmarks_toolbar.png')
        firefox_menu_most_visited_pattern = Pattern('firefox_menu_most_visited.png')
        new_bookmark_pattern = Pattern('new_bookmark_created.png')
        if OSHelper.is_linux():
            new_window_pattern = Pattern('new_bookmark_popup.png')
        else:
            new_window_pattern = Bookmarks.StarDialog.NEW_BOOKMARK

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

        right_click(firefox_menu_most_visited_pattern)

        new_bookmark_option_exists = exists(Library.Organize.NEW_BOOKMARK, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert new_bookmark_option_exists is True, 'Open in a New Bookmark option exists'

        click(Library.Organize.NEW_BOOKMARK)

        new_bookmark_window_exists = exists(new_window_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_bookmark_window_exists is True, 'New Bookmark window is displayed'

        click_cancel_button()

        try:
            new_bookmark_window_dismissed = wait_vanish(new_window_pattern)
            assert new_bookmark_window_dismissed is True, 'The popup is dismissed'
        except FindError:
            raise FindError('The popup is not dismissed.')

        open_bookmarks_toolbar()

        new_bookmark_not_added = exists(new_bookmark_pattern)
        assert new_bookmark_not_added is False, 'The New Bookmark window is dismissed and no bookmark is created.'
