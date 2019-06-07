# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This is a test of the sorting options from the sidebar - By Most Visited.',
        locale=['en-US'],
        test_case_id='119447',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        history_sidebar_view_button_pattern = Sidebar.HistorySidebar.VIEW_BUTTON
        history_sidebar_sort_by_date_pattern = Sidebar.HistorySidebar.ViewBy.VIEW_BY_DATE_CHECKED
        history_sidebar_sort_by_most_visited_pattern = Sidebar.HistorySidebar.ViewBy.VIEW_BY_MOST_VISITED
        history_sidebar_items_sorted_pattern = Pattern('history_sidebar_items_sort_by_most_visited.png')

        # Open some pages to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_test_site = exists(LocalWeb.MOZILLA_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert mozilla_test_site is True, 'Mozilla page loaded successfully.'

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_test_site = exists(LocalWeb.MOZILLA_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert mozilla_test_site is True, 'Mozilla page loaded successfully.'

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        firefox_test_site = exists(LocalWeb.FIREFOX_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert firefox_test_site is True, 'Firefox page loaded successfully.'

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)

        focus_test_site = exists(LocalWeb.FOCUS_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert focus_test_site is True, 'Focus page loaded successfully.'

        new_tab()
        navigate(LocalWeb.POCKET_TEST_SITE)

        pocket_test_site = exists(LocalWeb.POCKET_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert pocket_test_site is True, 'Pocket page loaded successfully.'

        # Open the History sidebar.
        history_sidebar()

        history_today_sidebar = exists(history_today_sidebar_pattern, Settings.FIREFOX_TIMEOUT)
        assert history_today_sidebar is True, 'Expand history sidebar button displayed properly.'

        click(history_today_sidebar_pattern)

        # Sort by date.
        history_sidebar_view_button = exists(history_sidebar_view_button_pattern, Settings.FIREFOX_TIMEOUT)
        assert history_sidebar_view_button is True, 'View button displayed properly.'

        click(history_sidebar_view_button_pattern)

        history_sidebar_sort_by_date = exists(history_sidebar_sort_by_date_pattern, Settings.FIREFOX_TIMEOUT)
        assert history_sidebar_sort_by_date is True, 'Default sorting option - sort by date - is selected properly.'

        # Sort by most visited.
        history_sidebar_sort_by_most_visited = exists(history_sidebar_sort_by_most_visited_pattern,
                                                      Settings.FIREFOX_TIMEOUT)
        assert history_sidebar_sort_by_most_visited is True, 'Sort by most visited option is displayed properly.'

        click(history_sidebar_sort_by_most_visited_pattern, 1)

        history_sidebar_items_sorted = exists(history_sidebar_items_sorted_pattern.similar(0.7),
                                              Settings.SITE_LOAD_TIMEOUT)
        assert history_sidebar_items_sorted is True, 'History list is sorted properly by most visited.'
