# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Open Library from Bookmarks menu"
        self.test_case_id = "163193"
        self.test_suite_id = "2525"
        self.locale = ["en-US"]

    def run(self):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        if Settings.is_linux() or Settings.is_mac():
            ff_menu_show_all_bookmarks_pattern = Pattern('ff_menu_show_all_bookmarks.png')
        else:
            ff_menu_show_all_bookmarks_pattern = Pattern('show_all_bookmarks_button.png')

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_menu_bookmarks_exists, 'Firefox menu > Bookmarks exists')

        click(firefox_menu_bookmarks_pattern)

        ff_menu_show_all_bookmarks_exists = exists(ff_menu_show_all_bookmarks_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, ff_menu_show_all_bookmarks_exists, 'Firefox menu > Bookmarks > Show All Bookmarks exists')

        click(ff_menu_show_all_bookmarks_pattern)

        library_opened_from_ff_menu = exists(Library.TITLE, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, library_opened_from_ff_menu, 'Library opened from View History, saved bookmarks and more')

        close_window_control('auxiliary')
