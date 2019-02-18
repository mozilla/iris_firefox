# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Delete items from \'Bookmarks Toolbar\''
        self.test_case_id = '164373'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        bookmarks_toolbar_menu_option_pattern = Pattern('bookmarks_toolbar_menu_option.png')
        iris_tab_pattern = Pattern('iris_tab.png')
        getting_started_toolbar_bookmark_pattern = Pattern('toolbar_bookmark_icon.png')
        bookmark_delete_option = Pattern('delete_bookmark.png')

        area_to_click = find(iris_tab_pattern)
        area_to_click.x += 300
        area_to_click.y += 5
        right_click(area_to_click)

        bookmarks_toolbar_menu_option_available = exists(bookmarks_toolbar_menu_option_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, bookmarks_toolbar_menu_option_available,
                    '\'Bookmarks Toolbar\' option is available in context menu')

        click(bookmarks_toolbar_menu_option_pattern)
        bookmarks_folder_available_in_toolbar = exists(getting_started_toolbar_bookmark_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, bookmarks_folder_available_in_toolbar, 'The \'Bookmarks Toolbar\' is enabled.')

        right_click(getting_started_toolbar_bookmark_pattern)
        delete_option_available = exists(bookmark_delete_option, DEFAULT_SYSTEM_DELAY)
        assert_true(self, delete_option_available,
                    '\'Delete\' option in available in context menu after right-click at the bookmark in toolbar.')

        click(bookmark_delete_option)
        bookmark_deleted = exists(getting_started_toolbar_bookmark_pattern, DEFAULT_UI_DELAY)
        assert_false(self, bookmark_deleted, 'The bookmark is deleted from the \'Bookmarks Toolbar\' section.')
