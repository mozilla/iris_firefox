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

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        library_button_pattern = NavBar.LIBRARY_MENU
        bookmarks_menu_option_pattern = LibraryMenu.BOOKMARKS_OPTION
        recently_wikipedia_bookmark_pattern = Pattern('recently_wikipedia_bookmark.png')
        wiki_bookmark_cut_pattern = Pattern('wiki_bookmark_cut.png')
        cut_option_pattern = Pattern('cut_option.png')

        library_button_exists = exists(library_button_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, library_button_exists, 'View history, saved bookmarks and more section exists')

        click(library_button_pattern)

        bookmarks_menu_option_exists = exists(bookmarks_menu_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarks_menu_option_exists, 'The Bookmarks menu is correctly displayed')

        click(bookmarks_menu_option_pattern)

        recently_wikipedia_bookmark_exists = exists(recently_wikipedia_bookmark_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, recently_wikipedia_bookmark_exists, 'Wikipedia bookmarks exists')

        right_click(recently_wikipedia_bookmark_pattern)

        cut_option_exists = exists(cut_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, cut_option_exists, 'Cut option exists')

        click(cut_option_pattern)

        wiki_bookmark_cut_exists = exists(wiki_bookmark_cut_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, wiki_bookmark_cut_exists, 'Cut option is grayed out.')


