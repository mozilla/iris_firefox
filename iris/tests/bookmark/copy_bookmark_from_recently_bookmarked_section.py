# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Copy a bookmark from the Recently Bookmarked section'
        self.test_case_id = '165490'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        library_button_pattern = NavBar.LIBRARY_MENU
        bookmarks_menu_option_pattern = LibraryMenu.BOOKMARKS_OPTION
        sidebar_bookmarks_header_pattern = SidebarBookmarks.BOOKMARKS_HEADER
        sidebar_bookmarks_toolbar_pattern = SidebarBookmarks.BOOKMARKS_TOOLBAR_MENU
        recently_wikipedia_bookmark_pattern = Pattern('recently_wikipedia_bookmark.png')
        wiki_sidebar_bookmark_pattern = Pattern('wiki_sidebar_bookmark.png')
        copy_option_pattern = Pattern('copy_option.png')
        paste_option_pattern = Pattern('paste_option.png')

        library_button_exists = exists(library_button_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, library_button_exists, 'View history, saved bookmarks and more section exists')

        click(library_button_pattern)

        bookmarks_menu_option_exists = exists(bookmarks_menu_option_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_menu_option_exists, 'The Bookmarks menu is correctly displayed')

        click(bookmarks_menu_option_pattern)

        recently_wikipedia_bookmark_exists = exists(recently_wikipedia_bookmark_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, recently_wikipedia_bookmark_exists, 'Wikipedia bookmarks exists')

        right_click(recently_wikipedia_bookmark_pattern)

        copy_option_exists = exists(copy_option_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, copy_option_exists, 'Copy option exists')

        click(copy_option_pattern)

        try:
            menu_disappeared = wait_vanish(copy_option_pattern, Settings.TINY_FIREFOX_TIMEOUT)
            assert_true(self, menu_disappeared, 'The selected website is correctly copied')
        except FindError:
            raise FindError('The selected website isn\'t correctly copied')

        bookmarks_sidebar('open')

        sidebar_bookmarks_header_exists = exists(sidebar_bookmarks_header_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, sidebar_bookmarks_header_exists, 'Bookmarks sidebar exists')

        sidebar_bookmarks_toolbar_exists = exists(sidebar_bookmarks_toolbar_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, sidebar_bookmarks_toolbar_exists, 'Bookmarks toolbar section exists')

        right_click(sidebar_bookmarks_toolbar_pattern)

        paste_option_exists = exists(paste_option_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, paste_option_exists, 'Paste option exists')

        click(paste_option_pattern)

        try:
            paste_option_disappeared = wait_vanish(paste_option_pattern, Settings.TINY_FIREFOX_TIMEOUT)
            assert_true(self, paste_option_disappeared, 'Paste option is gone')
        except FindError:
            raise FindError('Paste still exists')

        click(sidebar_bookmarks_toolbar_pattern)

        wiki_sidebar_bookmark_exists = exists(wiki_sidebar_bookmark_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, wiki_sidebar_bookmark_exists, 'The bookmark is correctly pasted in the selected section')