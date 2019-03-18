# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Delete a bookmark from the Recently Bookmarked section'
        self.test_case_id = '171647'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        getting_started_bookmark_pattern = Pattern('getting_started_bookmark.png')
        delete_bookmark_button_pattern = Pattern('delete_bookmark.png')

        click(NavBar.LIBRARY_MENU)

        bookmark_options_exists = exists(LibraryMenu.BOOKMARKS_OPTION)
        assert_true(self, bookmark_options_exists, 'Bookmark option is on display')

        click(LibraryMenu.BOOKMARKS_OPTION)

        bookmark_menu_exists = exists(getting_started_bookmark_pattern)
        assert_true(self, bookmark_menu_exists, 'The Bookmarks menu is correctly displayed')

        right_click(getting_started_bookmark_pattern)

        delete_bookmark_button_exists = exists(delete_bookmark_button_pattern)
        assert_true(self, delete_bookmark_button_exists, 'Delete button is displayed')

        click(delete_bookmark_button_pattern)

        try:
            website_bookmark_not_exists = wait_vanish(getting_started_bookmark_pattern)
            assert_true(self, website_bookmark_not_exists, 'The selected website is correctly deleted.')
        except FindError:
            raise FindError('The selected website is not deleted')
