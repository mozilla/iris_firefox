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
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        bookmarks_toolbar_most_visited_pattern = SidebarBookmarks.BookmarksToolbar.MOST_VISITED
        library_pattern = Library.TITLE
        history_pattern = Library.HISTORY
        copy_pattern = Pattern('copy.png')
        paste_pattern = Pattern('paste.png')
        history_bookmarks_toolbar_pattern = Pattern('history_bookmarks_toolbar.png')

        # Open the Bookmarks toolbar.
        open_bookmarks_toolbar()

        # Check that the Library window is displayed properly.
        open_library_menu(LibraryMenu.HISTORY_BUTTON)

        show_all_history_exists = exists(show_all_history_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, show_all_history_exists, '\"Show All History\" option exists.')

        click(show_all_history_pattern)

        library_displayed = exists(library_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, library_displayed, '\"Library\" window was displayed properly.')

        # Copy the history.
        history_item_exists = exists(history_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, history_item_exists, 'History item was found.')

        right_click(history_pattern)

        copy_option_exists = exists(copy_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, copy_option_exists, 'Copy option was found.')

        click(copy_pattern)

        click_window_control('close')

        # Paste the history.
        bookmarks_toolbar_most_visited_exists = exists(bookmarks_toolbar_most_visited_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_toolbar_most_visited_exists, 'Bookmarks Toolbar > Most Visited exists')

        right_click(bookmarks_toolbar_most_visited_pattern)

        paste_option_exists = exists(paste_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, paste_option_exists, 'Paste option was found.')

        click(paste_pattern)

        # Check that the history was copied.
        region = Region(0, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        history_copied = region.exists(history_bookmarks_toolbar_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, history_copied, 'History was successfully copied.')
