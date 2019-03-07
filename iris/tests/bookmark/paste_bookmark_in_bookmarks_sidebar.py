# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Paste a bookmark in Bookmarks Sidebar'
        self.test_case_id = '168935'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        copy_option_pattern = Pattern('copy_option.png')
        bookmark_from_library_pattern = Pattern('bookmark_from_library.png')
        bookmark_from_sidebar_pattern = Pattern('bookmark_from_sidebar.png')
        paste_option_pattern = Pattern('paste_option.png')

        if not Settings.is_mac():
            bookmarks_menu_pattern = Library.BOOKMARKS_MENU
        else:
            bookmarks_menu_pattern = Pattern('bookmark_menu_section.png')

        library_button_exists = exists(NavBar.LIBRARY_MENU, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, library_button_exists, 'Library button exists')

        click(NavBar.LIBRARY_MENU)

        library_menu_bookmarks_exists = exists(LibraryMenu.BOOKMARKS_OPTION, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, library_menu_bookmarks_exists, 'Library bookmarks section exists')

        click(LibraryMenu.BOOKMARKS_OPTION)

        bookmark_from_library_exists = exists(bookmark_from_library_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_from_library_exists, 'Bookmark from library exists')

        right_click(bookmark_from_library_pattern)

        copy_option_exists = exists(copy_option_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, copy_option_exists, 'Copy option exists')

        click(copy_option_pattern)

        try:
            bookmarks_is_copied = wait_vanish(copy_option_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
            assert_true(self, bookmarks_is_copied, 'The bookmark is correctly copied.')
        except FindError:
            raise FindError('Menu is still displayed')

        bookmarks_sidebar('open')

        bookmarks_sidebar_menu_header_exists = exists(SidebarBookmarks.BOOKMARKS_HEADER, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_sidebar_menu_header_exists, 'Bookmarks Sidebar is correctly displayed.')

        bookmarks_menu_exists = exists(bookmarks_menu_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_menu_exists, 'Bookmark Menu section exists')

        right_click(bookmarks_menu_pattern)

        paste_option_exists = exists(paste_option_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, paste_option_exists, 'Paste option exists')

        click(paste_option_pattern)

        try:
            paste_option_not_exists = wait_vanish(paste_option_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
            assert_true(self, paste_option_not_exists, 'Paste option disappeared')
        except FindError:
            raise FindError('Paste option still exists')

        click(bookmarks_menu_pattern)

        bookmark_from_sidebar_exists = exists(bookmark_from_sidebar_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_from_sidebar_exists, 'The bookmark is correctly copied in the selected section.')
