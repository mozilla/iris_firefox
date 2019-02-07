# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Paste a bookmark in \'Other Bookmarks\' section from Bookmarks menu'
        self.test_case_id = '171641'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        other_bookmarks_button_pattern = SidebarBookmarks.OTHER_BOOKMARKS
        bookmarks_menu_button_pattern = Library.BOOKMARKS_MENU
        copy_option_pattern = Pattern('copy_option.png')
        paste_option_pattern = Pattern('paste_option.png')
        wiki_favicon_bookmark_pattern = Pattern('wiki_bookmark_favicon.png')
        bookmarks_folder_pasted_pattern = Pattern('bookmarks_folder_pasted.png')

        if Settings.is_mac():
            type(text='b', modifier=KeyModifier.CMD + KeyModifier.SHIFT)
        elif Settings.is_windows():
            type(text='b', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)
        elif Settings.is_linux():
            type(text='o', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)

        other_bookmarks_button_available = exists(other_bookmarks_button_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, other_bookmarks_button_available,
                    '\'Other bookmarks\' button is available in \'Bookmarks Library\' menu.')

        click(other_bookmarks_button_pattern)
        bookmarks_displayed = exists(wiki_favicon_bookmark_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, bookmarks_displayed,
                    'The bookmarks saved in \'Other Bookmarks\' section are displayed.')

        bookmarks_menu_available = exists(bookmarks_menu_button_pattern, DEFAULT_UI_DELAY)
        assert_true(self, bookmarks_menu_available,
                    '\'Bookmarks menu\' button is available in \'Bookmarks Library\' menu.')

        right_click(bookmarks_menu_button_pattern)
        copy_option_available = exists(copy_option_pattern, DEFAULT_UI_DELAY)
        assert_true(self, copy_option_available,
                    '\'Copy\' option is available after right-click on the \'Bookmarks menu\' icon.')

        click(copy_option_pattern)
        right_click(other_bookmarks_button_pattern)
        paste_option_available = exists(paste_option_pattern, DEFAULT_UI_DELAY)
        assert_true(self, paste_option_available,
                    '\'Paste\' option is available after right-click on the \'Other Bookmarks\' folder icon.')

        click(paste_option_pattern)
        folder_pasted = exists(bookmarks_folder_pasted_pattern)
        assert_true(self, folder_pasted, 'The file/folder is correctly pasted in the \'Other Bookmarks\' section.')

        close_tab()
        close_window()
