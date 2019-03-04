# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Add a new Separator in 'Mozilla Firefox' section"
        self.test_case_id = "163375"
        self.test_suite_id = "2525"
        self.locale = ["en-US"]
        self.exclude = [Platform.MAC]

    def run(self):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        mozilla_firefox_predefined_bookmarks_pattern = Pattern('mozilla_firefox_predefined_bookmarks.png')
        mozilla_firefox_bookmarks_folder_pattern = Pattern('mozilla_firefox_bookmarks_folder.png')
        mozilla_about_us_bookmark_pattern = Pattern('mozilla_about_us_bookmark.png')
        separator_added_pattern = Pattern('separator_added.png')
        open_all_in_tabs_pattern = Pattern('open_all_in_tabs.png')

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

        new_separator_option_exists = exists(Library.Organize.NEW_SEPARATOR, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, new_separator_option_exists, 'New Folder option exists')

        click(Library.Organize.NEW_SEPARATOR)

        open_all_in_tabs_exists = exists(open_all_in_tabs_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, open_all_in_tabs_exists, 'Open all in tabs option exists')

        hover(open_all_in_tabs_pattern)

        separator_added = exists(separator_added_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, separator_added, 'A new Separator is added in Mozilla Firefox section.')

        restore_firefox_focus()
