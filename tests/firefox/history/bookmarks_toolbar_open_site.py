# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Copy a website from the History sidebar and paste it to the Bookmarks toolbar, then open it.',
        locale=['en-US'],
        test_case_id='120128',
        test_suite_id='2000',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):

        search_history_box_pattern = Sidebar.HistorySidebar.SEARCH_BOX
        sidebar_history_today_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        view_bookmarks_toolbar = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        bookmarks_toolbar_most_visited_pattern = SidebarBookmarks.BookmarksToolbar.MOST_VISITED
        if OSHelper.is_mac():
            bookmarks_toolbar_mozilla_pattern = Pattern('bookmarks_toolbar_mozilla.png')

        # Open a page to create some history.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_1, 'Mozilla page loaded successfully.'
        close_tab()

        # Open the Bookmarks toolbar.
        access_bookmarking_tools(view_bookmarks_toolbar)
        expected_2 = exists(bookmarks_toolbar_most_visited_pattern, 10)
        assert expected_2, 'Bookmarks Toolbar has been activated.'

        # Open the History sidebar.
        history_sidebar()
        expected_3 = exists(search_history_box_pattern, 10)
        assert expected_3, 'Sidebar was opened successfully.'
        expected_4 = exists(sidebar_history_today_pattern, 10)
        assert expected_4, 'Expand history button displayed properly.'
        click(sidebar_history_today_pattern)

        # Copy a website from the History sidebar and paste it to the Bookmarks toolbar.
        expected_5 = exists(LocalWeb.MOZILLA_BOOKMARK_SMALL, 10)
        assert expected_5, 'Mozilla page is displayed in the History list successfully.'

        right_click_and_type(LocalWeb.MOZILLA_BOOKMARK_SMALL, keyboard_action='c')

        history_sidebar()

        right_click_and_type(bookmarks_toolbar_most_visited_pattern, keyboard_action='p')

        if OSHelper.is_mac():
            expected_6 = exists(bookmarks_toolbar_mozilla_pattern)
        else:
            expected_6 = exists(LocalWeb.MOZILLA_BOOKMARK_SMALL)
        assert expected_6, 'Mozilla page was copied successfully to the Bookmarks toolbar.'

        # Open the site from the bookmarks toolbar
        if OSHelper.is_mac():
            click(bookmarks_toolbar_mozilla_pattern)
        else:
            click(LocalWeb.MOZILLA_BOOKMARK_SMALL)
        expected_7 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_7, 'Mozilla page loaded successfully.'
