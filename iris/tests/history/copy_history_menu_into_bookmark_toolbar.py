# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Copy the history menu and paste it into the Bookmark toolbar.'
        self.test_case_id = '174031'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        view_bookmarks_toolbar = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        bookmarks_toolbar_most_visited_pattern = SidebarBookmarks.BookmarksToolbar.MOST_VISITED
        library_pattern = Library.TITLE
        history_pattern = Library.HISTORY
        copy_pattern = Pattern('copy.png')
        paste_pattern = Pattern('paste.png')
        history_bookmarks_toolbar_pattern = Pattern('history_bookmarks_toolbar.png')

        # Open the Bookmarks toolbar.
        access_bookmarking_tools(view_bookmarks_toolbar)
        expected = exists(bookmarks_toolbar_most_visited_pattern, 10)
        assert_true(self, expected, 'Bookmarks Toolbar has been activated.')

        # Check that the Library window is displayed properly.
        open_library_menu('History')
        expected = exists(show_all_history_pattern, 10)
        assert_true(self, expected, '\"Show All History\" option exists.')
        click(show_all_history_pattern)
        expected = exists(library_pattern, 10)
        assert_true(self, expected, '\"Library\" window was displayed properly.')

        # Copy the history.
        expected = exists(history_pattern, 10)
        assert_true(self, expected, 'History item was found.')
        right_click(history_pattern)
        expected = exists(copy_pattern, 10)
        assert_true(self, expected, 'Copy option was found.')
        click(copy_pattern)

        click_window_control('close')
        time.sleep(DEFAULT_UI_DELAY)

        # Paste the history.
        right_click(bookmarks_toolbar_most_visited_pattern)
        expected = exists(paste_pattern, 10)
        assert_true(self, expected, 'Paste option was found.')
        click(paste_pattern)

        # Check that the history was copied.
        time.sleep(DEFAULT_UI_DELAY)
        region = Region(0, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        expected = region.exists(history_bookmarks_toolbar_pattern, 10)
        assert_true(self, expected, 'History was successfully copied.')
