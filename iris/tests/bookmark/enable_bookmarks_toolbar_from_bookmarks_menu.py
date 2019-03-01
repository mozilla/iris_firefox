# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bookmarks Toolbar can be enabled from the Bookmarks Menu.'
        self.test_case_id = '4089'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        bookmarks_toolbar_most_visited_pattern = SidebarBookmarks.BookmarksToolbar.MOST_VISITED

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_toolbar_pattern)

        enabled_toolbar_assert = exists(bookmarks_toolbar_most_visited_pattern, 10)
        assert_true(self, enabled_toolbar_assert, 'Bookmarks Toolbar has been activated.')
