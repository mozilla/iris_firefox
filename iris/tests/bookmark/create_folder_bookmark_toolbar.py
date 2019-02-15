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

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        add_new_bookmark_pattern = Library.Organize.NEW_BOOKMARK
        add_bookmark_panel_name_pattern = Bookmarks.StarDialog.NAME_FIELD
        folder_in_bookmarks_pattern = Pattern('folder_in_bookmarks_toolbar.png')
        mozilla_test_bookmark_pattern = Pattern('mozilla_test_bookmark.png')
        context_menu_bookmarks_toolbar_pattern = Pattern('bookmarks_toolbar_navbar_context_menu.png')
        add_bookmark_location_field_pattern = Pattern('add_bookmark_location_field.png')
        add_bookmark_popup_button_pattern = Pattern('add_button.png')

        home_button_displayed = exists(NavBar.HOME_BUTTON, DEFAULT_UI_DELAY)
        assert_true(self, home_button_displayed, 'Home button displayed')

        #  open Bookmark toolbar from bookmark section of Firefox menu
        home_button = NavBar.HOME_BUTTON
        w, h = home_button.get_size()
        horizontal_offset = w * 1.7
        vertical_offset = h * 2.1
        navbar_context_menu = home_button.target_offset(horizontal_offset, 0)
        navbar_add_bookmark_context_menu = home_button.target_offset(0, vertical_offset)

        right_click(navbar_context_menu)

        context_menu_bookmarks_toolbar = exists(context_menu_bookmarks_toolbar_pattern)
        assert_true(self, context_menu_bookmarks_toolbar, 'Context menu bookmarks toolbar option exists')
        click(context_menu_bookmarks_toolbar_pattern)

        # Fill in field and add bookmark
        right_click(navbar_add_bookmark_context_menu)

        add_new_bookmark = exists(add_new_bookmark_pattern)
        assert_true(self, add_new_bookmark, '"Add new bookmark" option exists')
        click(add_new_bookmark_pattern)

        add_bookmark_popup = exists(add_bookmark_panel_name_pattern)
        assert_true(self, add_bookmark_popup, 'Add bookmark popup loaded')

        click(add_bookmark_panel_name_pattern)
        paste('Test bookmark')

        add_bookmark_location_field = exists(add_bookmark_location_field_pattern)
        assert_true(self, add_bookmark_location_field, '"Add bookmark" popup loaded, and location field available')

        click(add_bookmark_location_field_pattern)
        paste('https://www.mozilla.org/en-US/firefox/central/')

        add_bookmark_popup_button = exists(add_bookmark_popup_button_pattern)
        assert_true(self, add_bookmark_popup_button, '"Add" button available')
        click(add_bookmark_popup_button_pattern)

        mozilla_test_bookmark = exists(mozilla_test_bookmark_pattern)
        assert_true(self, mozilla_test_bookmark, 'Mozilla test bookmark displayed')

        right_click(mozilla_test_bookmark_pattern)

        #  select Create new folder
        type('f', interval=DEFAULT_FX_DELAY)
        type(Key.ENTER)

        folder_created_in_bookmarks = exists(folder_in_bookmarks_pattern)
        assert_true(self, folder_created_in_bookmarks,
                    'The New Folder is correctly created in the Bookmarks Toolbar menu.')
