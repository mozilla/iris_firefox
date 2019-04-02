# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a bookmarked website by drag&drop'
        self.test_case_id = '164168'
        self.test_suite_id = '2525'
        self.locales = ['en-US']
        self.exclude = [Platform.MAC]

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        most_visited_bookmarks_folder_pattern = Pattern('most_visited_top_menu_bookmarks_folder.png')
        bookmarks_top_menu_toolbar_menu_item_pattern = Pattern('firefox_menu_bookmarks_toolbar.png')
        bookmarks_top_menu_option = Pattern('firefox_menu_bookmarks.png')
        pocket_bookmark_pattern = Pattern('pocket_most_visited.png')

        open_firefox_menu()

        bookmarks_option_available_in_top_menu = exists(bookmarks_top_menu_option, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_option_available_in_top_menu,
                    '\'Bookmarks\' menu item available in firefox top menu')

        click(bookmarks_top_menu_option)

        bookmarks_top_menu_toolbar_option_available = exists(bookmarks_top_menu_toolbar_menu_item_pattern)
        assert_true(self, bookmarks_top_menu_toolbar_option_available,
                    '\'Bookmarks toolbar\' option available in \'Bookmarks\' top menu section')

        mouse_move(bookmarks_top_menu_toolbar_menu_item_pattern)

        most_visited_bookmarks_folder_available = exists(most_visited_bookmarks_folder_pattern)
        assert_true(self, most_visited_bookmarks_folder_available,
                    '\'Most visited\' folder is available on the bookmarks toolbar')

        mouse_move(most_visited_bookmarks_folder_pattern)

        pocket_bookmark_available = exists(pocket_bookmark_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, pocket_bookmark_available,
                    '\'Pocket\' bookmark is available in \'Most visited\' '
                    'folder on the \'Bookmarks toolbar\' top menu section')

        drag_drop(pocket_bookmark_pattern, Location(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                  Settings.TINY_FIREFOX_TIMEOUT)

        bookmark_opened = exists(LocalWeb.POCKET_IMAGE, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, bookmark_opened, 'The selected website is correctly opened.')
