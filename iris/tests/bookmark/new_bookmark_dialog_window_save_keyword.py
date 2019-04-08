# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bug 1440644 - The New Bookmark dialog/window doesn\'t save the keyword'
        self.test_case_id = '171599'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        soap_bookmark_pattern = Pattern('soap_bookmark.png').similar(.6)
        new_bookmark_window_pattern = Pattern('new_bookmark_window.png')
        keyword_suggestion_pattern = Pattern('keyword_suggestion.png')

        open_library()

        library_opened = exists(Library.TITLE, Settings.FIREFOX_TIMEOUT)
        assert_true(self, library_opened, 'Library opened')

        other_bookmarks_folder_exists = exists(Library.OTHER_BOOKMARKS)
        assert_true(self, other_bookmarks_folder_exists, 'Other Bookmarks folder exists')

        other_bookmarks_width, other_bookmarks_height = Library.OTHER_BOOKMARKS.get_size()
        location_for_right_click = find(Library.OTHER_BOOKMARKS).right(other_bookmarks_width * 2)

        right_click(location_for_right_click)

        new_bookmark_option_exists = exists(Library.Organize.NEW_BOOKMARK)
        assert_true(self, new_bookmark_option_exists, 'New Bookmark option exists')

        click(Library.Organize.NEW_BOOKMARK)

        new_bookmark_window_opened = exists(new_bookmark_window_pattern)
        assert_true(self, new_bookmark_window_opened, 'New Bookmark window is displayed')

        paste('SOAP')
        type(Key.TAB)

        paste(LocalWeb.SOAP_WIKI_TEST_SITE)
        type(Key.TAB)

        paste('SOAP')
        if Settings.is_mac():
            type(Key.TAB)
        else:
            type(Key.TAB)
            type(Key.TAB)
        paste('y')

        type(Key.ENTER)

        bookmark_exists = exists(soap_bookmark_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, bookmark_exists, 'The new bookmark is added in the selected section')

        click(Library.TITLE)

        close_window_control('auxiliary')

        select_location_bar()

        type('y')

        suggestion_exists = exists(keyword_suggestion_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, suggestion_exists, 'The keyword search displays as first suggestion the bookmarked website.')
