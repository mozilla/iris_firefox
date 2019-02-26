# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Empty \'Recent Tags\' section from Bookmarks menu'
        self.test_case_id = '163220'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        global_menu_bookmarks_option_pattern = Pattern('global_menu_bookmarks_option.png')
        recent_tags_option_pattern = Pattern('recent_tags_option.png')
        empty_string_pattern = Pattern('empty.png')

        if Settings.is_windows():
            type(Key.ALT)
        elif Settings.is_linux():
            type(Key.F10)

        bookmarks_option_is_available_in_global_menu = exists(global_menu_bookmarks_option_pattern)
        assert_true(self, bookmarks_option_is_available_in_global_menu,
                    '\'Bookmarks\' option is available in global Firefox menu')

        click(global_menu_bookmarks_option_pattern)
        recent_tags_option_available = exists(recent_tags_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, recent_tags_option_available,
                    '\'Recent tags\' option available after clicking at \'Bookmarks option\' in global Firefox menu')

        mouse_move(recent_tags_option_pattern)
        empty_string_displayed = exists(empty_string_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, empty_string_displayed, 'Only the \'(Empty)\' string is displayed.')
