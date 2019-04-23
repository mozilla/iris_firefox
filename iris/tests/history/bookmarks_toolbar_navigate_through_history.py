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
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        bookmarks_toolbar_most_visited_pattern = SidebarBookmarks.BookmarksToolbar.MOST_VISITED
        history_pattern = Library.HISTORY
        iris_bookmark_pattern = Pattern('iris_bookmark.png')
        history_bookmarks_toolbar_pattern = Pattern('history_bookmarks_toolbar.png')
        copy_pattern = Pattern('copy.png')
        paste_pattern = Pattern('paste.png')

        # Open the Bookmarks toolbar.
        open_bookmarks_toolbar()

        # Open History and check if it is populated with the Iris page.
        open_library_menu(LibraryMenu.HISTORY_BUTTON)

        right_upper_corner = Region(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        iris_bookmark_exists = right_upper_corner.exists(iris_bookmark_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, iris_bookmark_exists, 'Iris page is displayed in the View History, saved bookmarks and more '
                                                '> History menu list.')

        show_all_history_exists = exists(show_all_history_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, show_all_history_exists, '\"Show All History\" option exists.')

        click(show_all_history_pattern)

        history_section_displayed = exists(history_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, history_section_displayed, 'Library > History section is visible.')

        right_click(history_pattern)

        copy_option_exists = exists(copy_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, copy_option_exists, 'Copy option was found.')

        click(copy_pattern)

        click_window_control('close')

        bookmarks_toolbar_most_visited_exists = exists(bookmarks_toolbar_most_visited_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_toolbar_most_visited_exists, 'Bookmarks Toolbar > Most Visited exists')

        right_click(bookmarks_toolbar_most_visited_pattern)

        paste_option_exists = exists(paste_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, paste_option_exists, 'Paste option was found.')

        click(paste_pattern)

        new_tab()

        history_section_pasted = exists(history_bookmarks_toolbar_pattern)
        assert_true(self, history_section_pasted, 'History section is pasted to the Bookmarks Toolbar.')

        click(history_bookmarks_toolbar_pattern)

        # Navigate to a page from Today's history, in our case the Iris page.
        type(Key.DOWN)
        type(Key.RIGHT)
        type(Key.ENTER)

        expected = exists(LocalWeb.IRIS_LOGO, Settings.FIREFOX_TIMEOUT)
        assert_true(self, expected, 'All the history is displayed and the page is correctly opened.')
