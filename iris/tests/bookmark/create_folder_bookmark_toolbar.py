# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Create "New Folder..." from "Bookmarks Toolbar"'
        self.test_case_id = '171637'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        folder_in_bookmarks_pattern = Pattern('folder_in_bookmarks_toolbar.png')
        mozilla_bookmark_icon_pattern = Pattern('mozilla_bookmark_icon.png')
        context_menu_bookmarks_toolbar_pattern = Pattern('bookmarks_toolbar_navbar_context_menu.png')

        home_button_displayed = exists(NavBar.HOME_BUTTON, DEFAULT_UI_DELAY)
        assert_true(self, home_button_displayed, 'Home button displayed')

        #  open Bookmark toolbar from bookmark section of Firefox menu
        home_button = NavBar.HOME_BUTTON
        w, h = home_button.get_size()
        horizontal_offset = w * 1.7
        navbar_context_menu = home_button.target_offset(horizontal_offset, 0)

        right_click(navbar_context_menu)

        context_menu_bookmarks_toolbar = exists(context_menu_bookmarks_toolbar_pattern)
        assert_true(self, context_menu_bookmarks_toolbar, 'Context menu bookmarks toolbar option exists')
        click(context_menu_bookmarks_toolbar_pattern)

        mozilla_bookmark_icon = exists(mozilla_bookmark_icon_pattern)
        assert_true(self, mozilla_bookmark_icon, 'Mozilla bookmark icon displayed')

        right_click(mozilla_bookmark_icon_pattern)

        #  select Create new folder
        type('f', interval=DEFAULT_FX_DELAY)
        type(Key.ENTER)

        folder_created_in_bookmarks = exists(folder_in_bookmarks_pattern)
        assert_true(self, folder_created_in_bookmarks,
                    'The New Folder is correctly created in the Bookmarks Toolbar menu.')
