# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Paste a bookmark in 'Mozilla Firefox' section "
        self.test_case_id = "163378"
        self.test_suite_id = "2525"
        self.locale = ["en-US"]
        self.exclude = [Platform.MAC]

    def run(self):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        mozilla_firefox_predefined_bookmarks_pattern = Pattern('mozilla_firefox_predefined_bookmarks.png')
        mozilla_firefox_bookmarks_folder_pattern = Pattern('mozilla_firefox_bookmarks_folder.png')
        mozilla_about_us_bookmark_pattern = Pattern('mozilla_about_us_bookmark.png')
        copy_option_pattern = Pattern('copy_option.png')
        paste_option_pattern = Pattern('paste_option.png')
        getting_started_in_toolbar_pattern = Pattern('getting_started_top_menu.png')
        bookmarks_toolbar_folder_pattern = Pattern('bookmark_toolbar_top_menu.png')

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_menu_bookmarks_exists, 'Firefox menu > Bookmarks exists')

        click(firefox_menu_bookmarks_pattern)

        bookmarks_toolbar_folder_exists = exists(bookmarks_toolbar_folder_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_toolbar_folder_exists, 'Bookmarks toolbar folder exists')

        click(bookmarks_toolbar_folder_pattern)

        getting_started_bookmark_exists = exists(getting_started_in_toolbar_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, getting_started_bookmark_exists, 'Getting started bookmark exists')

        right_click(getting_started_in_toolbar_pattern)

        copy_option_exists = exists(copy_option_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, copy_option_exists, 'The Copy option exists')

        click(copy_option_pattern)

        mozilla_firefox_bookmarks_folder_exists = exists(mozilla_firefox_bookmarks_folder_pattern,
                                                         DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, mozilla_firefox_bookmarks_folder_exists, 'Firefox menu > Bookmarks > Mozilla Firefox '
                                                                   'bookmarks folder exists')

        click(mozilla_firefox_bookmarks_folder_pattern)

        mozilla_firefox_predefined_bookmarks_exists = exists(mozilla_firefox_predefined_bookmarks_pattern,
                                                             DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, mozilla_firefox_predefined_bookmarks_exists, 'Predefined Mozilla Firefox related bookmarks '
                                                                       'displayed')

        right_click(mozilla_about_us_bookmark_pattern)

        paste_option_exists = exists(paste_option_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, paste_option_exists, 'Paste option exists')

        click(paste_option_pattern)

        bookmark_pasted = exists(getting_started_in_toolbar_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_pasted, 'Bookmark is correctly pasted in selected section')

        restore_firefox_focus()
