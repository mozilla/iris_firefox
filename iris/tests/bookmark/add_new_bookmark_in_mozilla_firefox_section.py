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
        mozilla_firefox_bookmarks_folder_pattern = Pattern('mozilla_firefox_bookmarks_folder.png')
        mozilla_about_us_bookmark_pattern = Pattern('mozilla_about_us_bookmark.png')
        new_bookmark_window_pattern = Pattern('new_bookmark_window.png')
        new_soap_bookmark_pattern = Pattern('new_soap_bookmark.png')
        open_all_in_tabs_pattern = Pattern('open_all_in_tabs.png')
        customize_firefox_bookmark_pattern = Pattern('mozilla_customize_firefox_bookmark.png')
        get_involved_bookmark_pattern = Pattern('mozilla_get_involved_bookmark.png')
        help_and_tutorials_bookmark_pattern = Pattern('mozilla_help_and_tutorials_bookmark.png')

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_menu_bookmarks_exists, 'Firefox menu > Bookmarks exists')

        click(firefox_menu_bookmarks_pattern)

        mozilla_firefox_bookmarks_folder_exists = exists(mozilla_firefox_bookmarks_folder_pattern,
                                                         Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, mozilla_firefox_bookmarks_folder_exists, 'Firefox menu > Bookmarks > Mozilla Firefox '
                                                                   'bookmarks folder exists')
        click(mozilla_firefox_bookmarks_folder_pattern)

        mozilla_customize_firefox_bookmark_exists = exists(customize_firefox_bookmark_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, mozilla_customize_firefox_bookmark_exists, 'Customize Firefox bookmark is displayed')

        mozilla_get_involved_bookmark_exists = exists(get_involved_bookmark_pattern)
        assert_true(self, mozilla_get_involved_bookmark_exists, 'Get Involved bookmark is displayed')

        mozilla_help_and_tutorials_bookmark_exists = exists(help_and_tutorials_bookmark_pattern)
        assert_true(self, mozilla_help_and_tutorials_bookmark_exists, 'Help and Tutorials bookmark is displayed')

        mozilla_about_us_bookmark_exists = exists(mozilla_about_us_bookmark_pattern)
        assert_true(self, mozilla_about_us_bookmark_exists, 'About Us bookmark is displayed')

        open_all_in_tabs_exists = exists(open_all_in_tabs_pattern)
        assert_true(self, open_all_in_tabs_exists, 'Open all in tabs option exists')

        right_click(mozilla_about_us_bookmark_pattern)

        context_menu_new_bookmark_pattern_displayed = exists(Library.Organize.NEW_BOOKMARK, Settings.FIREFOX_TIMEOUT)
        assert_true(self, context_menu_new_bookmark_pattern_displayed, 'Context menu New Bookmark option is displayed')

        click(Library.Organize.NEW_BOOKMARK)

        new_bookmark_window_opened = exists(new_bookmark_window_pattern, Settings.FIREFOX_TIMEOUT)
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

        firefox_menu_bookmarks__second_exists = exists(firefox_menu_bookmarks_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_menu_bookmarks__second_exists, 'Firefox menu > Bookmarks exists')

        click(firefox_menu_bookmarks_pattern)

        mozilla_firefox_bookmarks_folder_second_exists = exists(mozilla_firefox_bookmarks_folder_pattern,
                                                                Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, mozilla_firefox_bookmarks_folder_second_exists, 'Firefox menu > Bookmarks > Mozilla Firefox '
                                                                          'bookmarks folder exists')
        click(mozilla_firefox_bookmarks_folder_pattern)

        bookmark_exists = exists(new_soap_bookmark_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_exists, 'A new bookmark is added in Mozilla Firefox section.')

        restore_firefox_focus()
