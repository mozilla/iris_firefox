# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Copy a website from the History sidebar and paste it to the Bookmarks toolbar.'
        self.test_case_id = '120127'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def run(self):
        search_history_box_pattern = Sidebar.HistorySidebar.SEARCH_BOX
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        view_bookmarks_toolbar = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        bookmarks_toolbar_most_visited_pattern = SidebarBookmarks.BookmarksToolbar.MOST_VISITED
        if Settings.is_mac():
            bookmarks_toolbar_mozilla_pattern = Pattern('bookmarks_toolbar_mozilla.png')

        # Open a page to create some history.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_1, 'Mozilla page loaded successfully.')
        close_tab()

        # Open the Bookmarks toolbar.
        access_bookmarking_tools(view_bookmarks_toolbar)
        expected_2 = exists(bookmarks_toolbar_most_visited_pattern, 10)
        assert_true(self, expected_2, 'Bookmarks Toolbar has been activated.')

        # Open the History sidebar.
        history_sidebar()
        expected_3 = exists(search_history_box_pattern, 10)
        assert_true(self, expected_3, 'Sidebar was opened successfully.')
        expected_4 = exists(history_today_sidebar_pattern, 10)
        assert_true(self, expected_4, 'Expand history button displayed properly.')
        click(history_today_sidebar_pattern)

        # Copy a website from the History sidebar and paste it to the Bookmarks toolbar.
        expected_5 = exists(LocalWeb.MOZILLA_BOOKMARK_SMALL, 10)
        assert_true(self, expected_5, 'Mozilla page is displayed in the History list successfully.')

        right_click(LocalWeb.MOZILLA_BOOKMARK_SMALL)
        type(text='c')
        history_sidebar()
        right_click(bookmarks_toolbar_most_visited_pattern)
        type(text='p')
        if Settings.is_mac():
            expected_6 = exists(bookmarks_toolbar_mozilla_pattern)
        else:
            expected_6 = exists(LocalWeb.MOZILLA_BOOKMARK_SMALL)
        assert_true(self, expected_6, 'Mozilla page was copied successfully to the Bookmarks toolbar.')
