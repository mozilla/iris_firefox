# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Cut a bookmark from the Bookmarks toolbar submenu'
        self.test_case_id = '163487'
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
        getting_started_pattern = Pattern('getting_started_top_menu.png')
        getting_started_toolbar_pattern = Pattern('getting_started_in_toolbar.png')
        cut_option_pattern = Pattern('cut_option.png')
        paste_option_pattern = Pattern('paste_option.png')
        firefox_menu_most_visited_pattern = Pattern('firefox_menu_most_visited.png')

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

        cut_option_exists = exists(cut_option_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, cut_option_exists, 'The Cut option exists')

        click(cut_option_pattern)

        restore_firefox_focus()

        open_library()

        bookmarks_menu_folder_exists = exists(Library.BOOKMARKS_MENU)
        assert_true(self, bookmarks_menu_folder_exists, 'Bookmarks menu folder exists')

        bookmarks_menu_width, bookmarks_menu_height = Library.BOOKMARKS_MENU.get_size()
        location_to_paste = find(Library.BOOKMARKS_MENU).right(bookmarks_menu_width * 2)

        click(Library.BOOKMARKS_MENU)

        right_click(location_to_paste)

        paste_option_exists = exists(paste_option_pattern)
        assert_true(self, paste_option_exists, 'Paste option exists')

        click(paste_option_pattern)

        click(Library.BOOKMARKS_MENU)

        bookmark_pasted = exists(getting_started_toolbar_pattern)
        assert_true(self, bookmark_pasted, 'The file from the previous step is pasted in the selected section')

        close_window_control('auxiliary')

        open_bookmarks_toolbar()

        bookmark_removed_from_toolbar = exists(getting_started_toolbar_pattern)
        assert_false(self, bookmark_removed_from_toolbar, 'The file/folder from the previous step is pasted in the '
                                                          'selected section and deleted from the previous one.')
