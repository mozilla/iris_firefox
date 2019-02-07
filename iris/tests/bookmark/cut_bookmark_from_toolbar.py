# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Cut a bookmark from the Bookmarks toolbar submenu.'
        self.test_case_id = '171638'
        self.test_suite_id = '2525'
        self.locale = ['en-US']
        self.exclude = [Platform.MAC, Platform.LINUX]

    def run(self):
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        cut_item_pattern = Pattern('cut_bookmark.png')
        paste_item_pattern = Pattern('paste_bookmark.png')
        getting_started_bookmark_pattern = Pattern('getting_started_bookmark.png')
        firefox_bookmarks_folder_pattern = Pattern('firefox_bookmarks_folder.png')
        open_all_pattern = Pattern('open_all.png')

        type(Key.ALT)
        firefox_menu_opened = exists(bookmarks_top_menu_pattern)
        assert_true(self, firefox_menu_opened, 'Firefox menu opened')
        click(bookmarks_top_menu_pattern)

        bookmarks_dropdown_opened = exists(Library.BOOKMARKS_TOOLBAR)
        assert_true(self, bookmarks_dropdown_opened, 'Bookmarks menu opened')
        click(Library.BOOKMARKS_TOOLBAR)

        right_click(getting_started_bookmark_pattern)

        click(cut_item_pattern)

        click(firefox_bookmarks_folder_pattern)
        right_click(open_all_pattern)

        click(paste_item_pattern)

        bookmark_in_new_place = exists(getting_started_bookmark_pattern)
        assert_true(self, bookmark_in_new_place, 'Bookmark is pasted in new place')

        click(Library.BOOKMARKS_TOOLBAR)

        bookmark_deleted_from_default = not exists(getting_started_bookmark_pattern)
        assert_true(self, bookmark_deleted_from_default, 'bookmark_deleted_from_default')

        click(NavBar.HAMBURGER_MENU)  # Needed for correct firefox exit
        click(NavBar.HOME_BUTTON)
