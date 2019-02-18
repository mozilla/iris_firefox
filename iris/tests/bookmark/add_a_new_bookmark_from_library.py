# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Add a New Bookmark from Library'
        self.test_case_id = '169261'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        soap_bookmark_pattern = Pattern('soap_bookmark.png')
        new_bookmark_option_pattern = Pattern('new_bookmark_option.png')
        new_bookmark_window_pattern = Pattern('new_bookmark_window.png')

        open_library()

        library_opened = exists(Library.TITLE, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, library_opened, 'Library opened')

        location_for_right_click = find(Library.OTHER_BOOKMARKS).right(200)

        right_click(location_for_right_click)

        new_bookmark_option_exists = exists(new_bookmark_option_pattern)
        assert_true(self, new_bookmark_option_exists, 'New Bookmark option exists')

        click(new_bookmark_option_pattern)

        new_bookmark_window_opened = exists(new_bookmark_window_pattern)
        assert_true(self, new_bookmark_window_opened, 'New Bookmark window opened')

        paste('SOAP')
        type(Key.TAB)
        paste(LocalWeb.SOAP_WIKI_TEST_SITE)
        type(Key.TAB)
        paste('SOAP')
        type(Key.TAB)
        paste('SOAP')
        type(Key.ENTER)

        bookmark_exists = exists(soap_bookmark_pattern)
        assert_true(self, bookmark_exists, 'Bookmark exists')

        click(Library.TITLE)
        close_window_control('auxiliary')

        close_window()

