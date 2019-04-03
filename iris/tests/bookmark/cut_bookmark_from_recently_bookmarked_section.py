# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Cut a bookmark from the Recently Bookmarked section '
        self.test_case_id = '165489'
        self.test_suite_id = '2525'
        self.locales = ['en-US']
        self.blocked_by = {'id': '1533339', 'platform': Platform.ALL}

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        cut_option_pattern = Pattern('cut_option.png')
        paste_option_pattern = Pattern('paste_option.png')
        firefox_bookmark_cut_pattern = Pattern('firefox_bookmark_cut.png')

        library_button_exists = exists(NavBar.LIBRARY_MENU, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, library_button_exists, 'View history, saved bookmarks and more section exists')

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_menu_option_exists, 'The Bookmarks menu is correctly displayed')

        click(LibraryMenu.BOOKMARKS_OPTION)

        recently_firefox_bookmark_exists = exists(LocalWeb.FIREFOX_BOOKMARK, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, recently_firefox_bookmark_exists, 'Firefox bookmark exists in recently bookmarked section')

        right_click(LocalWeb.FIREFOX_BOOKMARK)

        cut_option_exists = exists(cut_option_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, cut_option_exists, '\'Cut\' option exists')

        click(cut_option_pattern)

        firefox_bookmark_cut_exists = exists(firefox_bookmark_cut_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, firefox_bookmark_cut_exists, 'The selected bookmark is grayed out')

        open_library()

        library_exists = exists(Library.TITLE, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, library_exists, 'Library bookmark menu is opened')

        bookmarks_toolbar_exists = exists(Library.BOOKMARKS_TOOLBAR, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_toolbar_exists, 'Bookmarks toolbar section exists')

        right_click(Library.BOOKMARKS_TOOLBAR)

        paste_option_exists = exists(paste_option_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, paste_option_exists, 'Paste option exists')

        click(paste_option_pattern)

        firefox_bookmark_cut_exists = exists(LocalWeb.FIREFOX_BOOKMARK, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, firefox_bookmark_cut_exists,
                    'The bookmark is correctly added in the selected section and deleted from the previous one.')

        close_window_control('auxiliary')

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_menu_option_exists, 'The Bookmarks menu is correctly displayed')

        click(LibraryMenu.BOOKMARKS_OPTION)

        recently_firefox_bookmark_not_exists = exists(LocalWeb.FIREFOX_BOOKMARK, Settings.TINY_FIREFOX_TIMEOUT)
        assert_false(self, recently_firefox_bookmark_not_exists,
                     'Firefox bookmark cut from recently bookmarked section')
