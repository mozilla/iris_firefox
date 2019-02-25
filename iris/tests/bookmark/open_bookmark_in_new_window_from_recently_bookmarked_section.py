# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a bookmark in a New Window from the Recently Bookmarked section'
        self.test_case_id = '165487'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        library_button_pattern = NavBar.LIBRARY_MENU
        bookmarks_menu_option_pattern = LibraryMenu.BOOKMARKS_OPTION
        recently_wikipedia_bookmark_pattern = Pattern('recently_wikipedia_bookmark.png')
        new_tab_is_opened_pattern = Pattern('opened_in_new_tab.png').similar(0.95)
        wikipedia_content_pattern = Pattern('wikipedia_content.png')
        open_in_new_window_option_pattern = Pattern('open_in_new_window.png')

        library_button_exists = exists(library_button_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, library_button_exists, 'View history, saved bookmarks and more section exists')

        click(library_button_pattern)

        bookmarks_menu_option_exists = exists(bookmarks_menu_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarks_menu_option_exists, 'The Bookmarks menu is correctly displayed')

        click(bookmarks_menu_option_pattern)

        recently_wikipedia_bookmark_exists = exists(recently_wikipedia_bookmark_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, recently_wikipedia_bookmark_exists, 'Wikipedia bookmark exists in recently bookmarked section')

        right_click(recently_wikipedia_bookmark_pattern)

        open_in_new_window_option_exists = exists(open_in_new_window_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, open_in_new_window_option_exists, 'Open in new window option exists')

        click(open_in_new_window_option_pattern)

        wikipedia_content_exists = exists(wikipedia_content_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, wikipedia_content_exists, 'Wikipedia content exists')

        new_tab_is_not_opened_exists = exists(new_tab_is_opened_pattern, DEFAULT_UI_DELAY_LONG)
        assert_false(self, new_tab_is_not_opened_exists, 'The selected website is opened in a new window.')

        close_window()
