# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Change the elements order in \'Bookmarks Toolbar\' with drag & drop.'
        self.test_case_id = '164378'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        bookmarks_toolbar_menu_option_pattern = Pattern('bookmarks_toolbar_menu_option.png')
        iris_tab_pattern = Pattern('iris_tab.png')
        most_visited_toolbar_bookmarks_folder_pattern = Pattern('drag_area.png')
        getting_started_toolbar_bookmark_pattern = Pattern('toolbar_bookmark_icon.png')
        toolbar_bookmarks_reordered_pattern = Pattern('toolbar_bookmarks_reordered.png')

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

        area_to_drop = find(most_visited_toolbar_bookmarks_folder_pattern)
        area_to_drop.x -= 1
        drag_drop(getting_started_toolbar_bookmark_pattern, area_to_drop)
        bookmarks_reordered = exists(toolbar_bookmarks_reordered_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, bookmarks_reordered, 'The position of the selected bookmark is changed as expected.')
