# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Add a new Separator in \'Mozilla Firefox\' section'
        self.test_case_id = '163375'
        self.test_suite_id = '2525'
        self.locale = ['en-US']
        self.exclude = [Platform.MAC]

    def run(self):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        mozilla_firefox_bookmarks_folder_pattern = Pattern('mozilla_firefox_bookmarks_folder.png')
        mozilla_about_us_bookmark_pattern = Pattern('mozilla_about_us_bookmark.png')
        separator_added_pattern = Pattern('separator_added.png')
        open_all_in_tabs_pattern = Pattern('open_all_in_tabs.png')
        customize_firefox_bookmark_pattern = Pattern('mozilla_customize_firefox_bookmark.png')
        get_involved_bookmark_pattern = Pattern('mozilla_get_involved_bookmark.png')
        help_and_tutorials_bookmark_pattern = Pattern('mozilla_help_and_tutorials_bookmark.png')

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_menu_bookmarks_exists, 'Firefox menu > Bookmarks button exists')

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

        new_separator_option_exists = exists(Library.Organize.NEW_SEPARATOR, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, new_separator_option_exists, 'New Folder option exists')

        click(Library.Organize.NEW_SEPARATOR)

        open_all_in_tabs_exists = exists(open_all_in_tabs_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, open_all_in_tabs_exists, 'Open all in tabs option exists')

        hover(open_all_in_tabs_pattern)

        separator_added = exists(separator_added_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, separator_added, 'A new Separator is added in Mozilla Firefox section.')

        restore_firefox_focus()
