# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bookmark a page from the bookmarks menu.'
        self.test_case_id = '165474'
        self.test_suite_id = '2525'
        self.exclude = Platform.ALL
        self.locales = ['en-US']

    def run(self):
        bookmark_this_page_pattern = Pattern('bookmark_this_page.png')
        blogger_logo_pattern = Pattern('blogger_logo.png')
        library_button_pattern = NavBar.LIBRARY_MENU
        bookmarks_menu_option_pattern = LibraryMenu.BOOKMARKS_OPTION
        star_button_unstarred_pattern = LocationBar.STAR_BUTTON_UNSTARRED
        star_button_starred_pattern = LocationBar.STAR_BUTTON_STARRED
        star_panel_pattern = Bookmarks.StarDialog.NEW_BOOKMARK

        navigate('www.blogger.com/')

        blogger_logo_exists = exists(blogger_logo_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, blogger_logo_exists, 'Website is properly loaded')

        library_button_exists = exists(library_button_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, library_button_exists, 'View history, saved bookmarks and more section exists')
        click(library_button_pattern)

        bookmarks_menu_option_exists = exists(bookmarks_menu_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmarks_menu_option_exists, 'Bookmarks menu option exists')
        click(bookmarks_menu_option_pattern)

        star_button_unstarred_exists = exists(star_button_unstarred_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, star_button_unstarred_exists, 'Unstarred star-shaped button exists')

        bookmark_menu_is_displayed = exists(bookmark_this_page_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, bookmark_menu_is_displayed, 'The Bookmarks menu is correctly displayed')
        click(bookmark_this_page_pattern)

        star_button_starred_exists = exists(star_button_starred_pattern, DEFAULT_UI_DELAY_LONG)
        assert_true(self, star_button_starred_exists, 'Star-shaped button changed its color to blue')

        bookmarks_menu_option_exists = exists(bookmarks_menu_option_pattern, DEFAULT_UI_DELAY_LONG)
        assert_false(self, bookmarks_menu_option_exists, 'Bookmarks menu is dismissed')

        star_panel_exists = exists(star_panel_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, star_panel_exists, 'Page Bookmarked menu is displayed under the star-shaped button.')

        star_panel_not_exists = exists(star_panel_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_false(self, star_panel_not_exists, 'Page Bookmarked menu is auto dismissed if no action is taken.')









