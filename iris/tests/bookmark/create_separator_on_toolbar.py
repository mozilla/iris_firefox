# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Create \'New Separator\' from \'Bookmarks Toolbar\''
        self.test_case_id = '164370'
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
        new_separator_option_pattern = Pattern('new_separator_option.png')
        bookmark_separator_pattern = Pattern('bookmark_separator.png')

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
        new_separator_option_available = exists(new_separator_option_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, new_separator_option_available,
                    '\'New separator\' option is available in context menu after right click at the bookmark')

        click(new_separator_option_pattern)
        try:
            context_menu_closed = wait_vanish(new_separator_option_pattern)
            assert_true(self, context_menu_closed, 'Context menu successfully closed after adding the separator')
        except FindError:
            raise FindError('Context menu didn\'t close after adding the separator for a bookmark')

        separator_added = exists(bookmark_separator_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, separator_added, 'A separator is displayed in front of the selected bookmark.')
