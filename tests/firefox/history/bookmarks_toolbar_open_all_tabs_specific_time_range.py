# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open all tabs from a specific time range saved in Bookmark Toolbar.',
        locale=['en-US'],
        test_case_id='174035',
        test_suite_id='2000'
    )
    def run(self, firefox):
        iris_tab_icon = Pattern('iris_logo_tab.png')
        mozilla_tab_icon = Pattern('mozilla_logo_tab.png')
        iris_bookmark_pattern = Pattern('iris_bookmark.png')
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        history_today_pattern = Library.HISTORY_TODAY
        new_tab_pattern = Pattern('new_tab.png')
        privacy_url = "http://www.mozilla.org/en-US/privacy/firefox/"
        firefox_privacy_logo_pattern = Pattern('firefox_privacy_logo_for_bookmarks.png')
        view_bookmarks_toolbar = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        bookmarks_toolbar_most_visited_pattern = SidebarBookmarks.BookmarksToolbar.MOST_VISITED
        today_bookmarks_toolbar_pattern = Pattern('today_bookmarks_toolbar.png')

        # Open the Bookmarks toolbar.
        access_bookmarking_tools(view_bookmarks_toolbar)

        expected = exists(bookmarks_toolbar_most_visited_pattern, 10)
        assert expected, 'Bookmarks Toolbar has been activated.'

        # Open a page to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected, 'Mozilla page loaded successfully.'

        new_tab()
        previous_tab()
        close_tab()

        navigate(privacy_url)
        new_tab()
        previous_tab()
        close_tab()

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

        expected = exists(history_today_pattern.similar(0.6), 10)
        assert expected, 'Today history option is available.'

        right_click_and_type(history_today_pattern, keyboard_action='c')

        click_window_control('close')
        time.sleep(Settings.DEFAULT_UI_DELAY)

        right_click_and_type(bookmarks_toolbar_most_visited_pattern, keyboard_action='p')

        expected = exists(today_bookmarks_toolbar_pattern)
        assert expected, 'Today time range was copied successfully to the Bookmarks toolbar.'

        # Right click on Today time range and select the Open All in Tabs button.
        right_click_and_type(today_bookmarks_toolbar_pattern, keyboard_action='o')

        # Make sure that all the pages from the selected history time range are opened in the current window.
        expected = exists(iris_tab_icon, 10)
        assert expected, 'Iris local page loaded successfully.'

        expected = exists(mozilla_tab_icon, 10)
        assert expected, 'Mozilla page loaded successfully.'

        expected = exists(firefox_privacy_logo_pattern, 10)
        assert expected, 'Firefox Privacy Notice page loaded successfully.'

        expected = exists(new_tab_pattern, 10)
        assert expected, 'about:newtab page loaded successfully.'
