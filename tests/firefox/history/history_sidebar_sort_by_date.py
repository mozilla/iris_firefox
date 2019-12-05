# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="This is a test of the sorting options from the sidebar - By Date.",
        locale=["en-US"],
        test_case_id="119446",
        test_suite_id="2000",
        profile=Profiles.BRAND_NEW,
        preferences={"browser.warnOnQuit": False, },
    )
    def run(self, firefox):
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        history_sidebar_view_button_pattern = Sidebar.HistorySidebar.VIEW_BUTTON
        history_sidebar_sort_by_date_pattern = Sidebar.HistorySidebar.ViewBy.VIEW_BY_DATE_CHECKED
        history_sidebar_items_sort_by_date_pattern = Pattern("history_sidebar_items_sort_by_date.png")

        # Open some pages to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_1 is True, "Mozilla page loaded successfully."

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected_2 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_2 is True, "Mozilla page loaded successfully."

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        expected_3 = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected_3 is True, "Firefox page loaded successfully."

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)

        expected_4 = exists(LocalWeb.FOCUS_LOGO, 10)
        assert expected_4 is True, "Focus page loaded successfully."

        new_tab()
        navigate(LocalWeb.POCKET_TEST_SITE)

        expected_5 = exists(LocalWeb.POCKET_LOGO, 10)
        assert expected_5 is True, "Pocket page loaded successfully."

        # Open the History sidebar.
        history_sidebar()

        expected_6 = exists(history_today_sidebar_pattern, 10)
        assert expected_6 is True, "Expand history sidebar button displayed properly."

        click(history_today_sidebar_pattern)

        # Sort by date.
        expected_7 = exists(history_sidebar_view_button_pattern, 10)
        assert expected_7 is True, "View button displayed properly."

        click(history_sidebar_view_button_pattern)

        expected_8 = exists(history_sidebar_sort_by_date_pattern, 10)
        assert expected_8 is True, "Default sorting option - sort by date - is selected properly."

        click(history_sidebar_sort_by_date_pattern)

        expected_9 = exists(history_sidebar_items_sort_by_date_pattern)
        assert expected_9 is True, "History list is sorted properly by date."
