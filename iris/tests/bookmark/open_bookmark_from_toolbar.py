# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a bookmark in a New Tab'
        self.test_case_id = '164363'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        most_visited_folder_pattern = Pattern('most_visited_bookmarks.png')
        pocket_bookmark_pattern = Pattern('pocket_bookmark_icon.png')
        open_option_pattern = Pattern('open_option.png')

        open_bookmarks_toolbar()

        bookmarks_folder_available_in_toolbar = exists(most_visited_folder_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_folder_available_in_toolbar, 'The \'Bookmarks Toolbar\' is enabled.')

        click(most_visited_folder_pattern)

        pocket_bookmark_available = exists(pocket_bookmark_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, pocket_bookmark_available,
                    '\'Pocket\' bookmark is available in the \'Most visited\' folder from the toolbar')

        right_click(pocket_bookmark_pattern)

        open_option_available = exists(open_option_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, open_option_available,
                    '\'Open\' option is available in context menu after right-click at the bookmark')

        click(open_option_pattern)

        website_opened_in_current_tab = exists(LocalWeb.POCKET_IMAGE, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, website_opened_in_current_tab, 'The website is correctly opened in the current tab.')

        bookmark_opened_in_current_tab = exists(LocalWeb.IRIS_LOGO_ACTIVE_TAB, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_false(self, bookmark_opened_in_current_tab,
                     'The page that was previously displayed in the current tab is no longer displayed')
