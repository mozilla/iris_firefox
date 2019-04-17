# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search for available bookmarks from Bookmarks Toolbar menu by tag'
        self.test_case_id = '166039'
        self.test_suite_id = '2525'
        self.locales = ['en-US']
        self.exclude = [Platform.MAC]

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        focused_url_bar_with_asterisk_pattern = Pattern('focused_url_address_bar_with_asterisk')

        click(NavBar.LIBRARY_MENU)

        library_menu_opened = exists(LibraryMenu.BOOKMARKS_OPTION, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, library_menu_opened, 'The Bookmarks menu is correctly displayed.')

        click(LibraryMenu.BOOKMARKS_OPTION)

        search_bookmarks_option_available = exists(Library.SEARCH_BOOKMARKS, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, search_bookmarks_option_available,
                    '\'Search bookmarks\' option from \'Bookmarks\' toolbar menu')

        click(Library.SEARCH_BOOKMARKS)

        menu_opened = exists(Library.SEARCH_BOOKMARKS)
        assert_false(self, menu_opened, 'The menu is dismissed')

        url_bar_focused = exists(focused_url_bar_with_asterisk_pattern)
        assert_true(self, url_bar_focused, 'The focus is in the URL address bar after a \'*\'.')
