# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Add a new bookmark in 'Mozilla Firefox' section "
        self.test_case_id = "163373"
        self.test_suite_id = "2525"
        self.locale = ["en-US"]
        self.exclude = [Platform.MAC]

    def run(self):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        mozilla_firefox_predefined_bookmarks_pattern = Pattern('mozilla_firefox_predefined_bookmarks.png')
        mozilla_firefox_bookmarks_folder_pattern = Pattern('mozilla_firefox_bookmarks_folder.png')
        mozilla_about_us_bookmark_pattern = Pattern('mozilla_about_us_bookmark.png')
        new_bookmark_window_pattern = Pattern('new_bookmark_window.png')
        new_soap_bookmark_pattern = Pattern('new_soap_bookmark.png')

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_menu_bookmarks_exists, 'Firefox menu > Bookmarks exists')

        click(firefox_menu_bookmarks_pattern)

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

        context_menu_new_bookmark_pattern_displayed = exists(Library.Organize.NEW_BOOKMARK, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, context_menu_new_bookmark_pattern_displayed, 'Context menu New Bookmark option is displayed')

        click(Library.Organize.NEW_BOOKMARK)

        new_bookmark_window_opened = exists(new_bookmark_window_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, new_bookmark_window_opened, 'New Bookmark window is displayed')

        paste('SOAP')
        type(Key.TAB)
        paste(LocalWeb.SOAP_WIKI_TEST_SITE)
        type(Key.TAB)
        paste('SOAP')
        type(Key.TAB)
        type(Key.TAB)
        paste('SOAP')
        type(Key.ENTER)

        open_firefox_menu()

        firefox_menu_bookmarks__second_exists = exists(firefox_menu_bookmarks_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_menu_bookmarks__second_exists, 'Firefox menu > Bookmarks exists')

        click(firefox_menu_bookmarks_pattern)

        mozilla_firefox_bookmarks_folder_second_exists = exists(mozilla_firefox_bookmarks_folder_pattern,
                                                                DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, mozilla_firefox_bookmarks_folder_second_exists, 'Firefox menu > Bookmarks > Mozilla Firefox '
                                                                          'bookmarks folder exists')
        click(mozilla_firefox_bookmarks_folder_pattern)

        bookmark_exists = exists(new_soap_bookmark_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_exists, 'A new bookmark is added in Mozilla Firefox section.')

        restore_firefox_focus()
