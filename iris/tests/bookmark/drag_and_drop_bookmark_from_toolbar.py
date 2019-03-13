# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Drag and drop a bookmark from \'Bookmark Toolbar\''
        self.test_case_id = '164377'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):

        pocket_logo_pattern = LocalWeb.POCKET_LOGO
        bookmarks_toolbar_menu_option_pattern = Pattern('bookmarks_toolbar_menu_option.png')
        most_visited_toolbar_bookmarks_folder_pattern = Pattern('drag_area.png')
        pocket_bookmark_pattern = Pattern('pocket_most_visited.png')
        iris_tab_pattern = Pattern('iris_tab.png')

        area_to_click = find(iris_tab_pattern)
        area_to_click.x += 300
        area_to_click.y += 5
        right_click(area_to_click)

        bookmarks_toolbar_menu_option_available = exists(bookmarks_toolbar_menu_option_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, bookmarks_toolbar_menu_option_available,
                    '\'Bookmarks Toolbar\' option is available in context menu')

        click(bookmarks_toolbar_menu_option_pattern)
        bookmarks_folder_available_in_toolbar = exists(most_visited_toolbar_bookmarks_folder_pattern,
                                                       DEFAULT_SYSTEM_DELAY)
        assert_true(self, bookmarks_folder_available_in_toolbar, 'The \'Bookmarks Toolbar\' is enabled.')

        click(most_visited_toolbar_bookmarks_folder_pattern)
        bookmark_available_in_folder = exists(pocket_bookmark_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, bookmark_available_in_folder,
                    '\'Pocket\' bookmark is displayed in \'Most visited\' bookmarks folder in toolbar')

        drag_drop(pocket_bookmark_pattern, area_to_click)
        select_tab(2)
        bookmarked_website_loaded = exists(pocket_logo_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, bookmarked_website_loaded, 'The selected website is correctly opened.')
