# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Copy a History time range from the History sidebar and paste it to the Bookmarks toolbar.'
        self.test_case_id = '120125'
        self.test_suite_id = '2000'

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.LIKE_NEW
        return

    def run(self):
        search_history_box_pattern = Pattern('search_history_box.png')
        expand_button_history_sidebar_pattern = Pattern('expand_button_history_sidebar.png')
        view_bookmarks_toolbar = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        bookmarks_toolbar_most_visited_pattern = SidebarBookmarks.BookmarksToolbar.MOST_VISITED
        today_bookmarks_toolbar_pattern = Pattern('today_bookmarks_toolbar.png')

        # Open a page to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_1, 'Mozilla page loaded successfully.')

        # Open the Bookmarks toolbar.
        access_bookmarking_tools(view_bookmarks_toolbar)
        expected_2 = exists(bookmarks_toolbar_most_visited_pattern, 10)
        assert_true(self, expected_2, 'Bookmarks Toolbar has been activated.')

        # Open the History sidebar.
        history_sidebar()
        expected_3 = exists(search_history_box_pattern, 10)
        assert_true(self, expected_3, 'Sidebar was opened successfully.')
        expected_4 = exists(expand_button_history_sidebar_pattern, 10)
        assert_true(self, expected_4, 'Expand history button displayed properly.')

        # Copy the History time range from the History sidebar and paste it to the Bookmarks toolbar.
        right_click(expand_button_history_sidebar_pattern)
        type(text='c')
        right_click(bookmarks_toolbar_most_visited_pattern)
        type(text='p')
        expected_5 = exists(today_bookmarks_toolbar_pattern)
        assert_true(self, expected_5, 'History time range was copied successfully to the Bookmarks toolbar.')
