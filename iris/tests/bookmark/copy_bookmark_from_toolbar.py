# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Copy items from \'Bookmarks Toolbar\''
        self.test_case_id = '164372'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        bookmarks_toolbar_menu_option_pattern = Pattern('bookmarks_toolbar_menu_option.png')
        bookmark_in_other_bookmarks_folder_pattern = Pattern('bookmark_in_folder.png')
        other_bookmarks_folder_pattern = Pattern('other_bookmarks_library_folder.png')
        getting_started_bookmark_pattern = Pattern('getting_started_bookmark.png')
        paste_option_pattern = Pattern('paste_option.png')
        copy_option_pattern = Pattern('copy_option.png')
        iris_tab_pattern = Pattern('iris_tab.png')

        area_to_click = find(iris_tab_pattern)
        area_to_click.x += 300
        area_to_click.y += 5
        right_click(area_to_click)

        bookmarks_toolbar_menu_option_available = exists(bookmarks_toolbar_menu_option_pattern)
        assert_true(self, bookmarks_toolbar_menu_option_available,
                    '\'Bookmarks Toolbar\' option is available in context menu')

        click(bookmarks_toolbar_menu_option_pattern)
        bookmark_available_in_toolbar = exists(getting_started_bookmark_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmark_available_in_toolbar, 'The \'Bookmarks Toolbar\' is enabled.')

        right_click(getting_started_bookmark_pattern)
        copy_option_available = exists(copy_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, copy_option_available,
                    '\'Copy\' option is available in context menu after right-click at the bookmark')

        click(copy_option_pattern)
        if Settings.is_mac():
            type(text='b', modifier=KeyModifier.CMD + KeyModifier.SHIFT)
        elif Settings.is_windows():
            type(text='b', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)
        elif Settings.is_linux():
            type(text='o', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)

        other_bookmarks_folder_available = exists(other_bookmarks_folder_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, other_bookmarks_folder_available,
                    '\'Other bookmarks\' folder is available in Library window')

        right_click(other_bookmarks_folder_pattern)
        paste_option_available = exists(paste_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, paste_option_available,
                    '\'Paste\' option is available in context menu after right-click at the bookmarks folder')

        click(paste_option_pattern)
        bookmark_pasted_into_folder = exists(bookmark_in_other_bookmarks_folder_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmark_pasted_into_folder,
                    'The bookmark from the previous step is pasted in the selected section.')

        close_tab()  # for closing Library window
