# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Delete a history time range from the Library.',
        locale=['en-US'],
        test_case_id='174036',
        test_suite_id='2000'
    )
    def run(self, firefox):
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        iris_bookmark_pattern = Pattern('iris_bookmark.png')
        iris_bookmark_focus_pattern = Pattern('iris_bookmark_focus.png')
        bookmarks_toolbar_most_visited_pattern = SidebarBookmarks.BookmarksToolbar.MOST_VISITED
        view_bookmarks_toolbar = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
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

        # Right click on a History time range (e.g. 'Today') and select Delete.
        history_today = exists(history_today_pattern.similar(0.6), FirefoxSettings.FIREFOX_TIMEOUT)
        assert history_today, 'History Today button available'

        history_today_location = find(history_today_pattern)
        history_today_width, history_today_height = history_today_pattern.get_size()
        history_today_region = Region(history_today_location.x, history_today_location.y,
                                      history_today_width, history_today_height)

        history_today = exists('Today', FirefoxSettings.FIREFOX_TIMEOUT, history_today_region)
        assert history_today, 'History Today button available'

        right_click_and_type(history_today_pattern.similar(0.6), keyboard_action='d')

        time.sleep(FirefoxSettings.SHORT_FIREFOX_TIMEOUT)

        history_today = not exists('Today', FirefoxSettings.FIREFOX_TIMEOUT, history_today_region)
        assert history_today, 'History Today button available'

        click_window_control('close')
