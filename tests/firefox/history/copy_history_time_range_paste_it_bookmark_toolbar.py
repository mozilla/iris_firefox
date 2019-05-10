# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Copy a history time range from the Library and paste it into the Bookmark Toolbar.',
        locale=['en-US'],
        test_case_id='174034',
        test_suite_id='2000'
    )
    def run(self, firefox):
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        iris_bookmark_pattern = Pattern('iris_bookmark.png')
        iris_bookmark_focus_pattern = Pattern('iris_bookmark_focus.png')
        bookmarks_toolbar_most_visited_pattern = SidebarBookmarks.BookmarksToolbar.MOST_VISITED
        view_bookmarks_toolbar = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        today_bookmarks_toolbar_pattern = Pattern('today_bookmarks_toolbar.png')
        history_today_pattern = Library.HISTORY_TODAY

        # Open the Bookmarks toolbar.
        access_bookmarking_tools(view_bookmarks_toolbar)

        expected = exists(bookmarks_toolbar_most_visited_pattern, 10)
        assert expected, 'Bookmarks Toolbar has been activated.'

        # Open History and check if it is populated with the Iris page.
        open_library_menu('History')

        right_upper_corner = Screen().new_region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2,
                                                 Screen.SCREEN_HEIGHT / 2)

        expected = right_upper_corner.exists(iris_bookmark_pattern, 10)
        assert expected, 'Iris page is displayed in the History menu list.'

        try:
            wait(show_all_history_pattern, 10)
            logger.debug('Show All History option found.')
            click(show_all_history_pattern)
        except FindError:
            raise FindError('Show All History option is not present on the page, aborting.')

        expected = exists(iris_bookmark_focus_pattern, 10)
        assert expected, 'Iris page is displayed in the Recent History list.'

        # Copy the History time range from the Library and paste it to the Bookmarks toolbar.

        right_click_and_type(history_today_pattern, keyboard_action='c')

        click_window_control('close')

        time.sleep(Settings.DEFAULT_UI_DELAY)

        right_click_and_type(bookmarks_toolbar_most_visited_pattern, keyboard_action='p')

        expected = exists(today_bookmarks_toolbar_pattern)
        assert expected, 'History time range was copied successfully to the Bookmarks toolbar.'
