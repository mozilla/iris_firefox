# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Clear Recent History from a predefined time range.'
        self.test_case_id = '172044'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def run(self):
        history_items_old_pattern = Pattern('history_items_old.png')
        history_title_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        if Settings.is_mac():
            clear_recent_history_last_hour_pattern = History.CLearRecentHistory.TimeRange.CLEAR_CHOICE_LAST_HOUR

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_1, 'Mozilla page loaded successfully.')

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        expected_2 = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected_2, 'Firefox page loaded successfully.')

        history_sidebar()
        # Open the 'Clear Recent History' window and uncheck all the items.
        for step in open_clear_recent_history_window():
            assert_true(self, step.resolution, step.message)

        if Settings.is_mac():
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
            assert_true(self, expected_4, 'Today\'s history was removed successfully.')
        except FindError:
            raise FindError('Today\'s history is still present.')
        expected_5 = exists(history_items_old_pattern, 10)
        assert_true(self, expected_5, 'Old history is still displayed properly.')
