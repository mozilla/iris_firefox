# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Paste a bookmark in \'Other Bookmarks\' section from Bookmarks menu'
        self.test_case_id = '163217'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        bookmarks_toolbar_folder_pattern = Pattern('bookmarks_toolbar_folder.png')
        getting_started_bookmark_pattern = Pattern('toolbar_bookmark_icon.png')
        other_bookmarks_folder_pattern = Pattern('other_bookmarks_folder.png')
        paste_option_pattern = Pattern('paste_option.png')
        copy_option_pattern = Pattern('copy_option.png')

        if Settings.is_mac():
            type(text='b', modifier=KeyModifier.CMD + KeyModifier.SHIFT)
        elif Settings.is_windows():
            type(text='b', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)
        elif Settings.is_linux():
            type(text='o', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)

        bookmarks_toolbar_folder_available = exists(bookmarks_toolbar_folder_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, bookmarks_toolbar_folder_available,
                    '\'Bookmarks toolbar\' button is available in \'Bookmarks Library\' menu.')

        other_bookmarks_folder_available = exists(other_bookmarks_folder_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, other_bookmarks_folder_available,
                    '\'Other bookmarks\' button is available in \'Bookmarks Library\' menu.')

        click(bookmarks_toolbar_folder_pattern)
        bookmarks_displayed = exists(getting_started_bookmark_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, bookmarks_displayed,
                    'The bookmarks saved in \'Bookmarks toolbar\' section are displayed.')

        right_click(getting_started_bookmark_pattern)
        copy_option_available = exists(copy_option_pattern, DEFAULT_UI_DELAY)
        assert_true(self, copy_option_available,
                    '\'Copy\' option is available after right-click on the \'Bookmarks toolbar\' icon.')

        click(copy_option_pattern)
        right_click(other_bookmarks_folder_pattern)
        paste_option_available = exists(paste_option_pattern, DEFAULT_UI_DELAY)
        assert_true(self, paste_option_available,
                    '\'Paste\' option is available after right-click on the \'Other Bookmarks\' folder icon.')

        click(paste_option_pattern)
        folder_pasted = exists(getting_started_bookmark_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, folder_pasted, 'The file/folder is correctly pasted in the \'Other Bookmarks\' section.')
