# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a bookmark in a New Private Window from Library'
        self.test_case_id = '169260'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        open_new_private_window_pattern = Pattern('open_in_private_window.png')
        bookmark_menu_pattern = Library.BOOKMARKS_MENU
        private_window_pattern = PrivateWindow.private_window_pattern

        if not Settings.is_mac():
            mozilla_bookmark_pattern = Pattern('mozilla_bookmark.png')
            bookmark_site_pattern = Pattern('bookmark_site.png')
        else:
            mozilla_bookmark_pattern = Pattern('mozilla_firefox_bookmark.png')
            bookmark_site_pattern = Pattern('website_bookmark_from_library.png')

        open_library()

        library_is_displayed = exists(bookmark_menu_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, library_is_displayed, 'Library is correctly open')

        click(bookmark_menu_pattern)

        mozilla_bookmark_exists = exists(mozilla_bookmark_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, mozilla_bookmark_exists, 'Mozilla bookmark exists')

        double_click(mozilla_bookmark_pattern)

        bookmark_site_exists = exists(bookmark_site_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, bookmark_site_exists, 'Website bookmark exists')

        right_click(bookmark_site_pattern)

        open_new_private_window_exists = exists(open_new_private_window_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, open_new_private_window_exists, 'Open new private window button exists')

        click(open_new_private_window_pattern)

        private_window_exists = exists(private_window_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, private_window_exists, 'The selected bookmark page is opened in a new private window.')

        close_window()
        close_window_control('auxiliary')
