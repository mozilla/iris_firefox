# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test of the Sorting options from the sidebar - By Date and Site.'
        self.test_case_id = '119444'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW

        return

    def run(self):
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        history_sidebar_view_button_pattern = Sidebar.HistorySidebar.VIEW_BUTTON
        history_sidebar_sort_by_date_pattern = Sidebar.HistorySidebar.ViewBy.VIEW_BY_DATE_CHECKED
        history_sidebar_sort_by_date_and_site_pattern = Sidebar.HistorySidebar.ViewBy.VIEW_BY_DATE_AND_SITE
        history_sidebar_items_sort_by_date_and_site_pattern = Pattern('history_sidebar_items_sort_by_date_and_site.png')

        # Open some pages to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_1, 'Mozilla page loaded successfully.')

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_2 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_2, 'Mozilla page loaded successfully.')

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        expected_3 = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected_3, 'Firefox page loaded successfully.')

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)
        expected_4 = exists(LocalWeb.FOCUS_LOGO, 10)
        assert_true(self, expected_4, 'Focus page loaded successfully.')

        new_tab()
        navigate(LocalWeb.POCKET_TEST_SITE)
        expected_5 = exists(LocalWeb.POCKET_LOGO, 10)
        assert_true(self, expected_5, 'Pocket page loaded successfully.')

        # Open the History sidebar.
        history_sidebar()
        expected_6 = exists(history_today_sidebar_pattern, 10)
        assert_true(self, expected_6, 'Expand history sidebar button displayed properly.')
        click(history_today_sidebar_pattern)

        # Sort by date by default.
        expected_7 = exists(history_sidebar_view_button_pattern, 10)
        assert_true(self, expected_7, 'View button displayed properly.')

        click(history_sidebar_view_button_pattern)
        expected_8 = exists(history_sidebar_sort_by_date_pattern, 10)
        assert_true(self, expected_8, 'Default sorting option - sort by date - is selected properly.')

        # Sort by date and site.
        expected_10 = exists(history_sidebar_sort_by_date_and_site_pattern, 10)
        assert_true(self, expected_10, 'Sort by date and site option is displayed properly.')

        click(history_sidebar_sort_by_date_and_site_pattern)
        expected_11 = exists(history_today_sidebar_pattern, 10)
        assert_true(self, expected_11, 'Expand history sidebar button displayed properly.')

        click(history_today_sidebar_pattern)
        expected_12 = exists(history_sidebar_items_sort_by_date_and_site_pattern)
        assert_true(self, expected_12, 'History list is sorted properly by date and site.')
