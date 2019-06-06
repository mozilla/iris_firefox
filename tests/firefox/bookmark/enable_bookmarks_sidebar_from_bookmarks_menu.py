# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmarks Sidebar can be enabled from the Bookmarks Menu.',
        locale=['en-US'],
        test_case_id='168920',
        test_suite_id='2525'
    )
    def run(self, firefox):
        view_bookmarks_sidebar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_SIDEBAR
        sidebar_other_bookmarks_pattern = SidebarBookmarks.OTHER_BOOKMARKS

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_sidebar_pattern)

        enabled_sidebar_assert = exists(sidebar_other_bookmarks_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert enabled_sidebar_assert is True, 'Bookmarks Sidebar has been enabled from the Bookmarks Menu.'
