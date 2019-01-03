# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Navigate through the History menu from the Bookmark toolbar.'
        self.test_case_id = '174032'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        Override the setup method to use a pre-canned bookmarks profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        iris_bookmark_pattern = Pattern('iris_bookmark.png')
        history_pattern = Library.HISTORY
        view_bookmarks_toolbar = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        bookmarks_toolbar_most_visited_pattern = SidebarBookmarks.BookmarksToolbar.MOST_VISITED
        iris_logo_pattern = Pattern('iris_logo.png')
        history_bookmarks_toolbar_pattern = Pattern('history_bookmarks_toolbar.png')

        # Open the Bookmarks toolbar.
        access_bookmarking_tools(view_bookmarks_toolbar)
        expected = exists(bookmarks_toolbar_most_visited_pattern, 10)
        assert_true(self, expected, 'Bookmarks Toolbar has been activated.')

        # Open History and check if it is populated with the Iris page.
        open_library_menu('History')

        right_upper_corner = Region(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        expected = right_upper_corner.exists(iris_bookmark_pattern, 10)
        assert_true(self, expected, 'Iris page is displayed in the History menu list.')

        click(show_all_history_pattern)

        expected = exists(history_pattern, 10)
        assert_true(self, expected, 'History section is visible.')

        right_click(history_pattern)
        type(text='c')

        click_window_control('close')
        time.sleep(DEFAULT_UI_DELAY)

        right_click(bookmarks_toolbar_most_visited_pattern)
        type(text='p')

        new_tab()
        expected = exists(history_bookmarks_toolbar_pattern)
        assert_true(self, expected, 'History section is displayed in the Bookmarks Toolbar.')

        click(history_bookmarks_toolbar_pattern)

        # Navigate to a page from Today's history, in our case the Iris page.
        type(Key.DOWN)
        type(Key.RIGHT)
        type(Key.ENTER)

        expected = exists(iris_logo_pattern, 10)
        assert_true(self, expected, 'Iris page successfully loaded.')
