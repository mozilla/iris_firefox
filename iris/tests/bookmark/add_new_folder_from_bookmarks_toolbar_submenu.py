# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Add a new folder from the Bookmarks Toolbar submenu'
        self.test_case_id = '163484'
        self.test_suite_id = '2525'
        self.locales = ['en-US']
        self.exclude = [Platform.MAC]

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        firefox_menu_bookmarks_toolbar_pattern = Pattern('firefox_menu_bookmarks_toolbar.png')
        firefox_menu_most_visited_pattern = Pattern('firefox_menu_most_visited.png')
        new_folder_pattern = Pattern('folder_in_bookmarks_toolbar.png')
        getting_started_pattern = Pattern('getting_started_top_menu.png')
        if Settings.is_linux():
            new_folder_window_pattern = Pattern('new_folder_bookmark.png')
        else:
            new_folder_window_pattern = Bookmarks.StarDialog.NEW_FOLDER_CREATED

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_menu_bookmarks_exists, 'Firefox menu > Bookmarks exists')

        click(firefox_menu_bookmarks_pattern)

        bookmarks_toolbar_folder_exists = exists(firefox_menu_bookmarks_toolbar_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_toolbar_folder_exists, 'Firefox menu > Bookmarks > Bookmarks Toolbar folder exists')

        click(firefox_menu_bookmarks_toolbar_pattern)

        most_visited_folder_exists = exists(firefox_menu_most_visited_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, most_visited_folder_exists, 'Firefox menu > Bookmarks > Bookmarks Toolbar > Most Visited '
                                                      'folder exists')

        getting_started_exists = exists(getting_started_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, getting_started_exists, 'Firefox menu > Bookmarks > Bookmarks Toolbar > Getting Started '
                                                  'bookmark exists')

        right_click(firefox_menu_most_visited_pattern)

        new_bookmark_option_exists = exists(Library.Organize.NEW_FOLDER, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, new_bookmark_option_exists, 'New Folder option exists')

        click(Library.Organize.NEW_FOLDER)

        new_folder_window_exists = exists(new_folder_window_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, new_folder_window_exists, 'New Folder window is displayed')

        type(Key.ENTER)

        try:
            new_folder_window_dismissed = wait_vanish(new_folder_window_pattern)
            assert_true(self, new_folder_window_dismissed, 'The popup is dismissed')
        except FindError:
            raise FindError('The popup is not dismissed.')

        open_bookmarks_toolbar()

        new_folder_added = exists(new_folder_pattern)
        assert_true(self, new_folder_added, 'The Folder is correctly added in the Bookmark Toolbar.')
