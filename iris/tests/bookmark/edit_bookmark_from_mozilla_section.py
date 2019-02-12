# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Edit a bookmark from \'Mozilla Firefox\' section'
        self.test_case_id = '163380'
        self.test_suite_id = '2525'
        self.locale = ['en-US']

    def run(self):
        bookmark_properties_pattern = Pattern('bookmark_properties.png')
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        customize_firefox_bookmark_pattern = Pattern('customize_firefox_bookmark.png')
        edited_bookmark_pattern = Pattern('edited_bookmark.png')
        firefox_bookmarks_folder_pattern = Pattern('firefox_bookmarks_folder.png')
        name_bookmark_field_pattern = Pattern('name_bookmark_field.png')

        type(Key.ALT)
        top_menu_displayed = exists(bookmarks_top_menu_pattern)
        assert_true(self, top_menu_displayed, 'Firefox menu is displayed')
        click(bookmarks_top_menu_pattern)

        bookmarks_dropdown_opened = exists(firefox_bookmarks_folder_pattern)
        assert_true(self, bookmarks_dropdown_opened, 'Bookmarks dropdown menu is opened')
        click(firefox_bookmarks_folder_pattern)

        default_bookmarks_displayed = exists(customize_firefox_bookmark_pattern)
        assert_true(self, default_bookmarks_displayed, 'Default bookmarks list is displayed')
        right_click(customize_firefox_bookmark_pattern)

        bookmark_dropdown_menu_opened = exists(bookmark_properties_pattern)
        assert_true(self, bookmark_dropdown_menu_opened, 'Bookmark dropdown menu is opened')
        click(bookmark_properties_pattern)

        bookmark_properties_displayed = exists(name_bookmark_field_pattern)
        assert_true(self, bookmark_properties_displayed, 'Bookmark properties are displayed')
        click(name_bookmark_field_pattern)
        edit_select_all()
        paste('qwert')
        type(Key.ENTER)

        type(Key.ALT)
        click(bookmarks_top_menu_pattern)
        click(firefox_bookmarks_folder_pattern)

        edited_tab_located = exists(edited_bookmark_pattern)
        assert_true(self, edited_tab_located, 'edited_tab_located')

        no_original_tab_located = not exists(customize_firefox_bookmark_pattern, DEFAULT_UI_DELAY)
        assert_true(self, no_original_tab_located, 'no_original_tab_located')

        click(NavBar.HAMBURGER_MENU)    # Is's required for correct process termination
        restore_firefox_focus()
