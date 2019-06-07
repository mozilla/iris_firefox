# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmark a page from the \'Most Visited\' section using the option from the contextual menu',
        locale=['en-US'],
        test_case_id='163202',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        firefox_menu_bookmarks_toolbar_pattern = Pattern('firefox_menu_bookmarks_toolbar.png')
        firefox_menu_most_visited_pattern = Pattern('firefox_menu_most_visited.png')
        firefox_pocket_bookmark_pattern = Pattern('pocket_most_visited.png')
        bookmark_page_option_pattern = Pattern('context_menu_bookmark_page_option.png')

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

        bookmark_page_option_exists = exists(bookmark_page_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmark_page_option_exists is True, 'Bookmark page option exists'

        click(bookmark_page_option_pattern)

        new_bookmark_window_exists = exists(Bookmarks.StarDialog.NAME_FIELD, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_bookmark_window_exists is True, 'New Bookmark window is displayed'

        paste('Focus')

        folders_expander_exists = exists(Bookmarks.StarDialog.PANEL_FOLDERS_EXPANDER.similar(.6),
                                         FirefoxSettings.FIREFOX_TIMEOUT)
        assert folders_expander_exists is True, 'Folders expander is displayed'

        click(Bookmarks.StarDialog.PANEL_FOLDERS_EXPANDER)

        bookmarks_toolbar_option_exists = exists(Library.BOOKMARKS_TOOLBAR,
                                                 FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmarks_toolbar_option_exists is True, 'Bookmark toolbar folder option is displayed'

        click(Library.BOOKMARKS_TOOLBAR)

        tags_field_exists = exists(Bookmarks.StarDialog.TAGS_FIELD, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert tags_field_exists is True, 'Tags field exists'

        click(Bookmarks.StarDialog.TAGS_FIELD)

        paste('tag')

        type(Key.ENTER)

        bookmark_added_to_toolbar = exists(LocalWeb.FOCUS_BOOKMARK_SMALL, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmark_added_to_toolbar is True, 'The bookmark is correctly added to Bookmarks Toolbar.'
