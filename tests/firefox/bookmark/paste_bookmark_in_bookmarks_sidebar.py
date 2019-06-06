# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Paste a bookmark in Bookmarks Sidebar',
        locale=['en-US'],
        test_case_id='168935',
        test_suite_id='2525'
    )
    def run(self, firefox):
        copy_option_pattern = Pattern('copy_option.png')
        bookmark_from_library_pattern = Pattern('bookmark_from_library.png')
        bookmark_from_sidebar_pattern = Pattern('bookmark_from_sidebar.png')
        paste_option_pattern = Pattern('paste_option.png')

        if not OSHelper.is_mac():
            bookmarks_menu_pattern = Library.BOOKMARKS_MENU
        else:
            bookmarks_menu_pattern = Pattern('bookmark_menu_section.png')

        library_button_exists = exists(NavBar.LIBRARY_MENU, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert library_button_exists is True, 'Library button exists'

        click(NavBar.LIBRARY_MENU)

        library_menu_bookmarks_exists = exists(LibraryMenu.BOOKMARKS_OPTION, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert library_menu_bookmarks_exists is True, 'Library bookmarks section exists'

        click(LibraryMenu.BOOKMARKS_OPTION)

        bookmark_from_library_exists = exists(bookmark_from_library_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmark_from_library_exists is True, 'Bookmark from library exists'

        right_click(bookmark_from_library_pattern)

        copy_option_exists = exists(copy_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert copy_option_exists is True, 'Copy option exists'

        click(copy_option_pattern)

        try:
            bookmarks_is_copied = wait_vanish(copy_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
            assert bookmarks_is_copied is True, 'The bookmark is correctly copied.'
        except FindError:
            raise FindError('Menu is still displayed')

        bookmarks_sidebar('open')

        bookmarks_sidebar_menu_header_exists = exists(SidebarBookmarks.BOOKMARKS_HEADER, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_sidebar_menu_header_exists is True, 'Bookmarks Sidebar is correctly displayed.'

        bookmarks_menu_exists = exists(bookmarks_menu_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_menu_exists is True, 'Bookmark Menu section exists'

        right_click(bookmarks_menu_pattern)

        paste_option_exists = exists(paste_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert paste_option_exists is True, 'Paste option exists'

        click(paste_option_pattern)

        try:
            paste_option_not_exists = wait_vanish(paste_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
            assert paste_option_not_exists is True, 'Paste option disappeared'
        except FindError:
            raise FindError('Paste option still exists')

        click(bookmarks_menu_pattern)

        bookmark_from_sidebar_exists = exists(bookmark_from_sidebar_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmark_from_sidebar_exists is True, 'The bookmark is correctly copied in the selected section.'
