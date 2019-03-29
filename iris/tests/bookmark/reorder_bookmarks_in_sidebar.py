# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Change the bookmarks order by drag&drop in \'Bookmarks Sidebar\''
        self.test_case_id = '168938'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        reordered_sidebar_bookmarks_pattern = Pattern('sidebar_bookmarks_reordered.png')
        pocket_bookmark_pattern = Pattern('pocket_sidebar_bookmark.png')
        mozilla_bookmark_pattern = Pattern('moz_sidebar_bookmark.png')
        other_bookmarks_pattern = Pattern('other_bookmarks_sidebar.png')

        bookmarks_sidebar('open')

        sidebar_opened = exists(other_bookmarks_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, sidebar_opened, '\'Bookmarks Sidebar\' is correctly displayed.')

        click(other_bookmarks_pattern)

        pocket_bookmark_available = exists(pocket_bookmark_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, pocket_bookmark_available,
                    '\'Pocket\' bookmark is available in \'Other bookmarks\' folder in \'Bookmarks sidebar\'')

        mozilla_bookmark_available = exists(mozilla_bookmark_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, mozilla_bookmark_available,
                    '\'Mozilla\' bookmark is available in \'Other bookmarks\' folder in \'Bookmarks sidebar\'')

        mozilla_bookmark_location = find(mozilla_bookmark_pattern)

        drag_drop(pocket_bookmark_pattern, mozilla_bookmark_location)

        bookmarks_not_reordered = exists(reordered_sidebar_bookmarks_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_not_reordered, 'The bookmarks order is correctly modified.')
