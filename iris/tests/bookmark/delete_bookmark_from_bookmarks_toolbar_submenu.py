# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Delete a bookmark from the Bookmarks Toolbar submenu'
        self.test_case_id = '163490'
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
        getting_started_pattern = Pattern('getting_started_top_menu.png')
        getting_started_toolbar_pattern = Pattern('getting_started_in_toolbar.png')
        delete_option_pattern = Pattern('delete_bookmark.png')

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

        right_click(getting_started_pattern)

        delete_option_exists = exists(delete_option_pattern)
        assert_true(self, delete_option_exists, 'Delete option exists')

        click(delete_option_pattern)

        try:
            getting_started_bookmark_removed = wait_vanish(getting_started_pattern)
            assert_true(self, getting_started_bookmark_removed, 'Getting Started bookmark deleted from Firefox menu >'
                                                                ' Bookmarks > Bookmarks Toolbar section')
        except FindError:
            raise FindError('Getting Started bookmark is not deleted')

        restore_firefox_focus()

        open_bookmarks_toolbar()

        bookmark_removed_from_toolbar = exists(getting_started_toolbar_pattern)
        assert_false(self, bookmark_removed_from_toolbar, 'The selected file is deleted from the **Bookmarks Toolbar**'
                                                          ' section.')
