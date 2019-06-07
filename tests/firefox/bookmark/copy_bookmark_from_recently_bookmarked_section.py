# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Copy a bookmark from the Recently Bookmarked section',
        locale=['en-US'],
        test_case_id='165490',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        library_button_pattern = NavBar.LIBRARY_MENU
        bookmarks_menu_option_pattern = LibraryMenu.BOOKMARKS_OPTION
        sidebar_bookmarks_header_pattern = SidebarBookmarks.BOOKMARKS_HEADER
        sidebar_bookmarks_toolbar_pattern = SidebarBookmarks.BOOKMARKS_TOOLBAR_MENU
        recently_wikipedia_bookmark_pattern = Pattern('recently_wikipedia_bookmark.png')
        wiki_sidebar_bookmark_pattern = Pattern('wiki_sidebar_bookmark.png')
        copy_option_pattern = Pattern('copy_option.png')
        paste_option_pattern = Pattern('paste_option.png')

        library_button_exists = exists(library_button_pattern)
        assert library_button_exists is True, 'View history, saved bookmarks and more section exists'

        click(library_button_pattern)

        bookmarks_menu_option_exists = exists(bookmarks_menu_option_pattern)
        assert bookmarks_menu_option_exists is True, 'The Bookmarks menu is correctly displayed'

        click(bookmarks_menu_option_pattern)

        recently_wikipedia_bookmark_exists = exists(recently_wikipedia_bookmark_pattern)
        assert recently_wikipedia_bookmark_exists is True, 'Wikipedia bookmarks exists'

        right_click(recently_wikipedia_bookmark_pattern)

        copy_option_exists = exists(copy_option_pattern)
        assert copy_option_exists is True, 'Copy option exists'

        click(copy_option_pattern)

        try:
            menu_disappeared = wait_vanish(copy_option_pattern)
            assert menu_disappeared is True, 'The selected website is correctly copied'
        except FindError:
            raise FindError('The selected website isn\'t correctly copied')

        bookmarks_sidebar('open')

        sidebar_bookmarks_header_exists = exists(sidebar_bookmarks_header_pattern)
        assert sidebar_bookmarks_header_exists  is True, 'Bookmarks sidebar exists'

        sidebar_bookmarks_toolbar_exists = exists(sidebar_bookmarks_toolbar_pattern)
        assert sidebar_bookmarks_toolbar_exists, 'Bookmarks toolbar section exists'

        right_click(sidebar_bookmarks_toolbar_pattern)

        paste_option_exists = exists(paste_option_pattern)
        assert paste_option_exists is True, 'Paste option exists'

        click(paste_option_pattern)

        try:
            paste_option_disappeared = wait_vanish(paste_option_pattern)
            assert paste_option_disappeared is True, 'Paste option is gone'
        except FindError:
            raise FindError('Paste still exists')

        click(sidebar_bookmarks_toolbar_pattern)

        wiki_sidebar_bookmark_exists = exists(wiki_sidebar_bookmark_pattern)
        assert wiki_sidebar_bookmark_exists is True, 'The bookmark is correctly pasted in the selected section'
