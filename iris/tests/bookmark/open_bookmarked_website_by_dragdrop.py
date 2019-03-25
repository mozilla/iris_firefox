# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a bookmarked website by drag&drop'
        self.test_case_id = '164168'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        getting_started_toolbar_bookmark_pattern = Pattern('mozilla_bookmark_icon.png')
        most_visited_bookmarks_folder_pattern = Pattern('most_visited_bookmarks.png')
        pocket_bookmark_pattern = Pattern('pocket_most_visited.png')

        open_bookmarks_toolbar()

        most_visited_bookmarks_folder_available = exists(most_visited_bookmarks_folder_pattern,
                                                         Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, most_visited_bookmarks_folder_available,
                    '\'Most visited\' folder is available on the bookmarks toolbar')

        getting_started_bookmark_available = exists(getting_started_toolbar_bookmark_pattern,
                                                    Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, getting_started_bookmark_available,
                    '\'Getting started\' bookmark is available on the bookmarks toolbar')

        click(most_visited_bookmarks_folder_pattern)

        pocket_bookmark_available = exists(pocket_bookmark_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, pocket_bookmark_available,
                    '\'Pocket\' bookmark is available in \'Most visited\' folder on the toolbar')

        drag_drop(pocket_bookmark_pattern, Location(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        bookmark_opened = exists(LocalWeb.POCKET_IMAGE, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, bookmark_opened, 'The selected website is correctly opened.')
