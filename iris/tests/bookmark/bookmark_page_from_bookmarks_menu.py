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
        self.locales = ['en-US']

    def run(self):
        bookmark_this_page_pattern = Pattern('bookmark_this_page.png')
        blogger_logo_pattern = Pattern('blogger_logo.png')

        navigate('www.blogger.com/')

        blogger_logo_exists = exists(blogger_logo_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, blogger_logo_exists, 'Website is properly loaded')

        library_button_exists = exists(NavBar.LIBRARY_MENU, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, library_button_exists, 'View history, saved bookmarks and more section exists')

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_menu_option_exists, 'Bookmarks menu option exists')

        click(LibraryMenu.BOOKMARKS_OPTION)

        star_button_unstarred_exists = exists(LocationBar.STAR_BUTTON_UNSTARRED, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, star_button_unstarred_exists, 'Unstarred star-shaped button exists')

        bookmark_menu_is_displayed = exists(bookmark_this_page_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_menu_is_displayed, 'The Bookmarks menu is correctly displayed')

        click(bookmark_this_page_pattern)

        star_button_starred_exists = exists(LocationBar.STAR_BUTTON_STARRED, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, star_button_starred_exists, 'Star-shaped button changed its color to blue')

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION, Settings.TINY_FIREFOX_TIMEOUT)
        assert_false(self, bookmarks_menu_option_exists, 'Bookmarks menu is dismissed')

        star_panel_exists = exists(Bookmarks.StarDialog.NEW_BOOKMARK, Settings.FIREFOX_TIMEOUT)
        assert_true(self, star_panel_exists, 'Page Bookmarked menu is displayed under the star-shaped button.')

        mouse_move(LocationBar.STAR_BUTTON_STARRED)

        try:
            star_panel_not_exists = wait_vanish(Bookmarks.StarDialog.NEW_BOOKMARK, Settings.FIREFOX_TIMEOUT)
            assert_true(self, star_panel_not_exists, 'Page Bookmarked menu is auto dismissed if no action is taken '
                                                     'and if the cursor outside the star-panel. ')
        except FindError:
            raise FindError('Page Bookmarked menu isn\'t auto dismissed')
