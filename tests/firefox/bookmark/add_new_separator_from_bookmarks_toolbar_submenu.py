# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Add a new Separator from the Bookmarks Toolbar submenu',
        locale=['en-US'],
        test_case_id='163486',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        firefox_menu_bookmarks_toolbar_pattern = Pattern('firefox_menu_bookmarks_toolbar.png')
        getting_started_pattern = Pattern('getting_started_top_menu.png')
        separator_added_pattern = Pattern('separator_added_to_toolbar.png')
        firefox_menu_most_visited_pattern = Pattern('firefox_menu_most_visited.png')

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

        new_separator_option_exists = exists(Library.Organize.NEW_SEPARATOR, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert new_separator_option_exists is True, 'New Separator option exists'

        click(Library.Organize.NEW_SEPARATOR)

        restore_firefox_focus()

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)

        open_bookmarks_toolbar()

        new_separator_added = exists(separator_added_pattern)
        assert new_separator_added is True, 'A separator is displayed in the front of the selected file in the' \
                                            ' Bookmark Toolbar.'
