# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Paste items from \'Bookmarks Toolbar\''
        self.test_case_id = '165204'
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
        copy_option_pattern = Pattern('copy_option.png')
        paste_option_pattern = Pattern('paste_option.png')
        two_identical_bookmarks_pattern = Pattern('bookmark_copied.png')

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
        cut_option_available_in_context_menu = exists(copy_option_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, cut_option_available_in_context_menu,
                    '\'Copy\' option is available after right click at the bookmark icon')

        click(copy_option_pattern)
        try:
            context_menu_closed = wait_vanish(paste_option_pattern)
            assert_true(self, context_menu_closed, 'Context menu successfully closed after copying the bookmark')
        except FindError:
            raise FindError('Context menu didn\'t close while copying the bookmark')

        area_to_paste = find(getting_started_toolbar_bookmark_pattern)
        area_to_paste.x += 150
        area_to_paste.y += 5
        right_click(area_to_paste)
        paste_option_available = exists(paste_option_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, paste_option_available, '\'Paste\' option is available after right click at the toolbar')

        click(paste_option_pattern)
        bookmark_copied = exists(two_identical_bookmarks_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, bookmark_copied, 'The item is correctly pasted in the select section.')
