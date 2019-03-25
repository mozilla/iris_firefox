# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Add a new Folder in \'Other Bookmarks\' section form Bookmarks menu'
        self.test_case_id = '163213'
        self.test_suite_id = '2525'
        self.locale = ['en-US']
        self.exclude = [Platform.MAC]

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        add_button_pattern = Pattern('add_button.png')
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        firefox_bookmark_top_menu_pattern = Pattern('firefox_bookmark_top_menu.png')
        folder_bookmarks_top_menu_pattern = Pattern('folder_bookmarks_top_menu.png')
        other_bookmarks_top_menu_pattern = Pattern('other_bookmarks.png')
        name_bookmark_field_pattern = Pattern('name_bookmark_field.png')
        new_folder_pattern = Pattern('new_folder.png')

        open_firefox_menu()

        firefox_menu_opened = exists(bookmarks_top_menu_pattern)
        assert_true(self, firefox_menu_opened, 'Firefox menu is displayed')

        click(bookmarks_top_menu_pattern)

        bookmarks_menu_opened = exists(other_bookmarks_top_menu_pattern)
        assert_true(self, bookmarks_menu_opened, 'Bookmarks top menu is displayed')

        click(other_bookmarks_top_menu_pattern)

        bookmarks_displayed = exists(firefox_bookmark_top_menu_pattern)
        assert_true(self, bookmarks_displayed, 'Previously saved bookmarks are saved')

        other_bookmarks_item_y = find(other_bookmarks_top_menu_pattern).y
        firefox_bookmark_item_y = find(firefox_bookmark_top_menu_pattern).y

        hover(Location(SCREEN_WIDTH, other_bookmarks_item_y))
        hover(Location(SCREEN_WIDTH, firefox_bookmark_item_y))

        right_click(firefox_bookmark_top_menu_pattern)

        context_menu_displayed = exists(new_folder_pattern)
        assert_true(self, context_menu_displayed, 'Context menu for bookmarks is displayed')

        click(new_folder_pattern)

        form_window_displayed = exists(name_bookmark_field_pattern)
        assert_true(self, form_window_displayed, 'Folder creation form properly displayed.')

        add_button_displayed = exists(add_button_pattern)
        assert_true(self, add_button_displayed, '"Add" button displayed')

        click(name_bookmark_field_pattern)

        paste('folder')

        add_button_displayed = exists(add_button_pattern)
        assert_true(self, add_button_displayed, '"Add" button displayed')

        click(add_button_pattern)

        open_firefox_menu()

        firefox_menu_opened = exists(bookmarks_top_menu_pattern)
        assert_true(self, firefox_menu_opened, 'Firefox menu is displayed')

        click(bookmarks_top_menu_pattern)

        bookmarks_menu_opened = exists(other_bookmarks_top_menu_pattern)
        assert_true(self, bookmarks_menu_opened, 'Bookmarks top menu is displayed')

        click(other_bookmarks_top_menu_pattern)

        folder_saved = exists(folder_bookmarks_top_menu_pattern)
        assert_true(self, folder_saved, 'The new folder is available in the Other Bookmarks section.')

        click(NavBar.HAMBURGER_MENU)

        restore_firefox_focus()
