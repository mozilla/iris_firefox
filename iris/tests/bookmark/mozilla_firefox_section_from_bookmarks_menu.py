# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Mozilla Firefox section from Bookmarks menu"
        self.test_case_id = "163229"
        self.test_suite_id = "2525"
        self.locale = ["en-US"]

    def run(self):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        mozilla_firefox_predefined_bookmarks_pattern = Pattern('mozilla_firefox_predefined_bookmarks.png')
        open_all_in_tabs_pattern = Pattern('open_all_in_tabs.png')
        mozilla_firefox_bookmarks_folder_pattern = Pattern('mozilla_firefox_bookmarks_folder.png')

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

        open_all_in_tabs_button_displayed = exists(open_all_in_tabs_pattern)
        assert_true(self, open_all_in_tabs_button_displayed, 'Open All in Tabs button is displayed')

        restore_firefox_focus()
