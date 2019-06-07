# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmarks Toolbar can be enabled from the Bookmarks Menu.',
        locale=['en-US'],
        test_case_id='4089',
        test_suite_id='2525'
    )
    def run(self, firefox):
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        bookmarks_toolbar_most_visited_pattern = SidebarBookmarks.BookmarksToolbar.MOST_VISITED

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_toolbar_pattern)

        enabled_toolbar_assert = exists(bookmarks_toolbar_most_visited_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert enabled_toolbar_assert is True, 'Bookmarks Toolbar has been activated.'
