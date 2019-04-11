# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test of the sorting options from the sidebar - By Site.'
        self.test_case_id = '119445'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW

    def run(self):
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        history_sidebar_view_button_pattern = Sidebar.HistorySidebar.VIEW_BUTTON
        history_sidebar_sort_by_date_pattern = Sidebar.HistorySidebar.ViewBy.VIEW_BY_DATE_CHECKED
        history_sidebar_sort_by_site_pattern = Sidebar.HistorySidebar.ViewBy.VIEW_BY_SITE
        history_sidebar_items_sort_by_site_pattern = Pattern('history_sidebar_items_sort_by_site.png')

        # Open some pages to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_test_site_loaded = exists(LocalWeb.MOZILLA_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, mozilla_test_site_loaded, 'Mozilla page loaded successfully.')

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_test_site_loaded = exists(LocalWeb.MOZILLA_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, mozilla_test_site_loaded, 'Mozilla page loaded successfully.')

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        firefox_test_site_loaded = exists(LocalWeb.FIREFOX_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, firefox_test_site_loaded, 'Firefox page loaded successfully.')

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)

        focus_test_site_loaded = exists(LocalWeb.FOCUS_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, focus_test_site_loaded, 'Focus page loaded successfully.')

        new_tab()
        navigate(LocalWeb.POCKET_TEST_SITE)

        pocket_test_site_loaded = exists(LocalWeb.POCKET_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, pocket_test_site_loaded, 'Pocket page loaded successfully.')

        # Open the History sidebar.
        history_sidebar()

        history_today_sidebar = exists(history_today_sidebar_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, history_today_sidebar, 'Expand history sidebar button displayed properly.')

        click(history_today_sidebar_pattern)

        # Sort by date by default.
        history_sidebar_view_button = exists(history_sidebar_view_button_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, history_sidebar_view_button, 'View button displayed properly.')

        click(history_sidebar_view_button_pattern)

        history_sidebar_sort_by_date = exists(history_sidebar_sort_by_date_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, history_sidebar_sort_by_date, 'Default sorting option - sort by date - is selected properly.')

        # Sort by site.
        history_sidebar_sort_by_site = exists(history_sidebar_sort_by_site_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, history_sidebar_sort_by_site, 'Sort by site option is displayed properly.')

        click(history_sidebar_sort_by_site_pattern)

        history_sidebar_items_sort_by_site = exists(history_sidebar_items_sort_by_site_pattern,
                                                    Settings.FIREFOX_TIMEOUT)
        assert_true(self, history_sidebar_items_sort_by_site, 'History list is sorted properly by site.')
