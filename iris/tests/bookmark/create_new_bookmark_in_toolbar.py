# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = ''
        self.test_case_id = ''
        self.test_suite_id = ''
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        bookmarks_toolbar_menu_option_pattern = Pattern('bookmarks_toolbar_menu_option.png')
        iris_tab_pattern = Pattern('iris_tab.png')
        getting_started_toolbar_bookmark_pattern = Pattern('toolbar_bookmark_icon.png')
        new_bookmark_option_pattern = Pattern('new_bookmark_option.png')
        location_field_pattern = Pattern('bookmark_location_field.png')
        new_bookmark_pattern = Pattern('new_bookmark.png')

        area_to_click = find(iris_tab_pattern)
        area_to_click.x += 300
        area_to_click.y += 5
        right_click(area_to_click)

        bookmarks_toolbar_menu_option_available = exists(bookmarks_toolbar_menu_option_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, bookmarks_toolbar_menu_option_available,
                    '\'Bookmarks Toolbar\' option is available in context menu')

        click(bookmarks_toolbar_menu_option_pattern)
        bookmark_available_in_toolbar = exists(getting_started_toolbar_bookmark_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, bookmark_available_in_toolbar, 'The \'Bookmarks Toolbar\' is enabled.')

        right_click(getting_started_toolbar_bookmark_pattern)
        new_bookmark_option_available = exists(new_bookmark_option_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, new_bookmark_option_available,
                    '\'New bookmark\' option is available in context menu after right click at the bookmark')

        click(new_bookmark_option_pattern)
        location_field_available = exists(location_field_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, location_field_available, 'A new bookmark window is opened.')

        click(location_field_pattern)
        paste('test')
        type(Key.ENTER)

        bookmark_added = exists(new_bookmark_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, bookmark_added, 'The new bookmark is displayed in the \'Bookmarks Toolbar\' menu.')

