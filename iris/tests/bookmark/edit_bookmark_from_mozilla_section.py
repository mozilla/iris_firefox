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
        customize_firefox_bookmark_pattern = Pattern('customize_firefox_bookmark.png')
        edited_bookmark_pattern = Pattern('edited_bookmark.png')
        firefox_bookmarks_folder_pattern = Pattern('firefox_bookmarks_folder.png')
        name_bookmark_field_pattern = Pattern('name_bookmark_field.png')

        if Settings.is_windows():
            bookmark_properties_pattern = Pattern('bookmark_properties.png')
            bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        elif Settings.is_mac():
            bookmarks_menu_pattern = Pattern('bookmarks_menu_library_icon.png')
        else:
            bookmarks_menu_pattern = Pattern('bookmarks_menu.png')

        if Settings.is_windows():
            type(Key.ALT)
            top_menu_displayed = exists(bookmarks_top_menu_pattern)
            assert_true(self, top_menu_displayed, 'Firefox menu is displayed')
            click(bookmarks_top_menu_pattern)
        else:
            open_library()
            library_opened = exists(bookmarks_menu_pattern)
            assert_true(self, library_opened, 'Library is opened')

            _, bookmarks_menu_height = bookmarks_menu_pattern.get_size()
            bookmarks_menu_height //= 2
            click(bookmarks_menu_pattern.target_offset(0, bookmarks_menu_height))

        bookmarks_folder_located = exists(firefox_bookmarks_folder_pattern)
        assert_true(self, bookmarks_folder_located, 'Mozilla Firefox bookmarks folder is found')

        click(firefox_bookmarks_folder_pattern)

        default_bookmarks_displayed = exists(customize_firefox_bookmark_pattern)
        assert_true(self, default_bookmarks_displayed, 'Default bookmarks list is displayed')

        if Settings.is_windows():
            right_click(customize_firefox_bookmark_pattern)
            bookmark_dropdown_menu_opened = exists(bookmark_properties_pattern)
            assert_true(self, bookmark_dropdown_menu_opened, 'Bookmark dropdown menu is opened')
            click(bookmark_properties_pattern)
        else:
            click(customize_firefox_bookmark_pattern)

        bookmark_properties_displayed = exists(name_bookmark_field_pattern)
        assert_true(self, bookmark_properties_displayed, 'Bookmark properties are displayed')

        click(name_bookmark_field_pattern)
        edit_select_all()
        paste('qwert')
        type(Key.ENTER)

        if Settings.is_windows():
            type(Key.ALT)
            click(bookmarks_top_menu_pattern)
            click(firefox_bookmarks_folder_pattern)

        edited_bookmark_located = exists(edited_bookmark_pattern)
        assert_true(self, edited_bookmark_located, 'Edited bookmark is located among default')

        no_original_bookmark_located = not exists(customize_firefox_bookmark_pattern, DEFAULT_UI_DELAY)
        assert_true(self, no_original_bookmark_located, 'Default "Custom Firefox" bookmark isn\'t found')

        if Settings.is_windows():
            click(NavBar.HAMBURGER_MENU)    # Is's required for correct process termination
            restore_firefox_focus()
        else:
            close_tab()
