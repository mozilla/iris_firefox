# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.nightly.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Clear all of the browser history.",
        locale=["en-US"],
        test_case_id="172045",
        test_suite_id="2000",
    )
    def run(self, firefox):
        searched_history_logo_pattern = Sidebar.HistorySidebar.EXPLORED_HISTORY_ICON.similar(
            0.9
        )
        if OSHelper.is_mac():
            clear_recent_history_last_hour_pattern = (
                History.ClearRecentHistory.TimeRange.CLEAR_CHOICE_LAST_HOUR
            )

        # Open some pages to create some history.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        reset_mouse()

        expected_1 = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert expected_1, "Mozilla page loaded successfully."

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        expected_2 = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert expected_2, "Firefox page loaded successfully."

        # Open the History sidebar.
        # history_sidebar()

        # Open the Clear Recent History window and select 'Everything'.
        for step in open_clear_recent_history_window():
            assert step.resolution, step.message
        if OSHelper.is_mac():
            click(clear_recent_history_last_hour_pattern)
            for i in range(4):
                type(Key.DOWN)
                time.sleep(Settings.DEFAULT_UI_DELAY)
            type(Key.ENTER)
            time.sleep(Settings.DEFAULT_UI_DELAY)

        else:
            for i in range(4):
                type(Key.DOWN)
                time.sleep(Settings.DEFAULT_UI_DELAY)

        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        # Sometimes Firefox is in a state where it can't receive keyboard input
        # and we need to restore the focus manually.
        restore_firefox_focus()

        # Open the History sidebar.
        history_sidebar()

        # Check that all the history was cleared.
        region_left = Screen.LEFT_THIRD
        try:
            region_left.wait_vanish(searched_history_logo_pattern, 10)
            logger.debug("All the history was cleared.")
        except FindError:
            raise FindError("All the history was not cleared successfully.")

        history_sidebar()
