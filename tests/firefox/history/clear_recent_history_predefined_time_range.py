# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Clear Recent History from a predefined time range.',
        locale=['en-US'],
        test_case_id='172044',
        test_suite_id='2000'
    )
    def run(self, firefox):
        history_items_old_pattern = Pattern('history_items_old.png')
        history_title_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        if OSHelper.is_mac():
            clear_recent_history_last_hour_pattern = History.CLearRecentHistory.TimeRange.CLEAR_CHOICE_LAST_HOUR

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert  expected_1, 'Mozilla page loaded successfully.'

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        expected_2 = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert  expected_2, 'Firefox page loaded successfully.'

        history_sidebar()
        # Open the 'Clear Recent History' window and uncheck all the items.
        for step in open_clear_recent_history_window():
            assert  step.resolution, step.message

        if OSHelper.is_mac():
            click(clear_recent_history_last_hour_pattern)
            type(Key.DOWN)
            type(Key.DOWN)
            type(Key.DOWN)
            type(Key.ENTER)
            type(Key.ENTER)

        else:
            type(Key.DOWN)
            type(Key.DOWN)
            type(Key.DOWN)
            type(Key.ENTER)

        try:
            expected_4 = wait_vanish(history_title_pattern, 10)
            assert expected_4, 'Today\'s history was removed successfully.'
        except FindError:
            raise FindError('Today\'s history is still present.')
        expected_5 = exists(history_items_old_pattern, 10)
        assert expected_5, 'Old history is still displayed properly.'
