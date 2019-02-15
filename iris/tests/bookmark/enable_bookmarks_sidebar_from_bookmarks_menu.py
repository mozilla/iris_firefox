# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bookmarks Sidebar can be enabled from the Bookmarks Menu.'
        self.test_case_id = '168920'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        view_bookmarks_sidebar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_SIDEBAR
        sidebar_other_bookmarks_pattern = SidebarBookmarks.OTHER_BOOKMARKS

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_sidebar_pattern)

        enabled_sidebar_assert = exists(sidebar_other_bookmarks_pattern, 10)
        assert_true(self, enabled_sidebar_assert, 'Bookmarks Sidebar has been enabled from the Bookmarks Menu.')
