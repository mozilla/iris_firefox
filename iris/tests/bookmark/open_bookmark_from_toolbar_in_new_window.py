# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a bookmark from toolbar in a New Window'
        self.test_case_id = '164365'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        open_in_new_window_option_pattern = Pattern('open_in_new_window_option.png')
        most_visited_toolbar_bookmarks_folder_pattern = Pattern('drag_area.png')
        pocket_bookmark_icon_pattern = Pattern('pocket_bookmark_icon.png')

        open_bookmarks_toolbar()

        bookmarks_folder_available_in_toolbar = exists(most_visited_toolbar_bookmarks_folder_pattern,
                                                       DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_folder_available_in_toolbar, 'The \'Bookmarks Toolbar\' is enabled.')

        click(most_visited_toolbar_bookmarks_folder_pattern)

        pocket_bookmark_available = exists(pocket_bookmark_icon_pattern, DEFAULT_TINY_FIREFOX_TIMEOUT)
        assert_true(self, pocket_bookmark_available,
                    '\'Pocket\' bookmark is available in the \'Most visited\' folder in toolbar')

        right_click(pocket_bookmark_icon_pattern)

        open_in_new_window_option_available = exists(open_in_new_window_option_pattern, DEFAULT_TINY_FIREFOX_TIMEOUT)
        assert_true(self, open_in_new_window_option_available,
                    '\'Open in new window\' option in available in context '
                    'menu after right-click at the bookmark in toolbar.')

        click(open_in_new_window_option_pattern)

        website_loaded = exists(LocalWeb.POCKET_IMAGE, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, website_loaded, 'The selected website is correctly opened in a new window.')

        close_window()

        iris_tab_displayed = exists(LocalWeb.IRIS_LOGO_ACTIVE_TAB, DEFAULT_TINY_FIREFOX_TIMEOUT)
        assert_true(self, iris_tab_displayed, '\'Iris\' tab remains available in the non-private window')
