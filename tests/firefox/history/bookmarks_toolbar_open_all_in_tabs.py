# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Copy a History time range from the History sidebar and paste it to the Bookmarks toolbar, then '
                    'use the \'Open All in Tabs\' option on the saved bookmark.',
        locale=['en-US'],
        test_case_id='120126',
        test_suite_id='2000'
    )
    def run(self, firefox):
        privacy_url = "http://www.mozilla.org/en-US/privacy/firefox/"
        search_history_box_pattern = Sidebar.HistorySidebar.SEARCH_BOX
        expand_button_history_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        view_bookmarks_toolbar = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        bookmarks_toolbar_most_visited_pattern = SidebarBookmarks.BookmarksToolbar.MOST_VISITED
        today_bookmarks_toolbar_pattern = Pattern('today_bookmarks_toolbar.png')
        firefox_privacy_logo_pattern = Pattern('firefox_privacy_logo_for_bookmarks.png')
        iris_tab_icon = Pattern('iris_logo_tab.png')
        mozilla_tab_icon = Pattern('mozilla_logo_tab.png')

        # Open a page to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_1, 'Mozilla page loaded successfully.'

        next_tab()
        navigate(privacy_url)

        close_content_blocking_pop_up()

        # Open the Bookmarks toolbar.
        access_bookmarking_tools(view_bookmarks_toolbar)

        expected_2 = exists(bookmarks_toolbar_most_visited_pattern, 10)
        assert expected_2, 'Bookmarks Toolbar has been activated.'

        # Open the History sidebar.
        history_sidebar()

        expected_3 = exists(search_history_box_pattern, 10)
        assert expected_3, 'Sidebar was opened successfully.'

        expected_4 = exists(expand_button_history_sidebar_pattern, 10)
        assert expected_4, 'Expand history button displayed properly.'

        # Copy the History time range from the History sidebar and paste it to the Bookmarks toolbar.
        right_click_and_type(expand_button_history_sidebar_pattern, keyboard_action='c')

        right_click_and_type(bookmarks_toolbar_most_visited_pattern, keyboard_action='p')

        expected_5 = exists(today_bookmarks_toolbar_pattern)
        assert expected_5, 'History time range was copied successfully to the Bookmarks toolbar.'

        # Click on the bookmark and select the Open All in Tabs button.
        right_click_and_type(today_bookmarks_toolbar_pattern, keyboard_action='o')

        # Check that all the pages loaded successfully.
        expected_6 = exists(firefox_privacy_logo_pattern, 10)
        assert expected_6, 'Firefox Privacy Notice loaded successfully.'

        expected_7 = exists(iris_tab_icon, 10)
        assert expected_7, 'Iris local page loaded successfully.'

        expected_8 = exists(mozilla_tab_icon, 10)
        assert expected_8, 'Mozilla page loaded successfully.'
