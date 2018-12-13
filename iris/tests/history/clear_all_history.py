# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Clear all the History.'
        self.test_case_id = '172045'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def run(self):
        history_empty_pattern = Pattern('history_empty.png')
        if Settings.is_mac():
            clear_recent_history_last_hour_pattern = History.CLearRecentHistory.TimeRange.CLEAR_CHOICE_LAST_HOUR

        # Open some pages to create some history.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_1, 'Mozilla page loaded successfully.')

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        expected_2 = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected_2, 'Firefox page loaded successfully.')

        # Open the History sidebar.
        history_sidebar()

        # Open the Clear Recent History window and select 'Everything'.
        for step in open_clear_recent_history_window():
            assert_true(self, step.resolution, step.message)
        if Settings.is_mac():
            click(clear_recent_history_last_hour_pattern)
            for i in range(4):
                type(Key.DOWN)
            type(Key.ENTER)

        else:
            for i in range(4):
                type(Key.DOWN)

        type(Key.TAB)
        type(Key.TAB)
        for i in range(5):
            type(Key.DOWN)
        type(Key.SPACE)
        type(Key.DOWN)
        type(Key.SPACE)
        type(Key.ENTER)

        # Sometimes Firefox is in a state where it can't receive keyboard input
        # and we need to restore the focus manually.
        restore_firefox_focus()

        # Check that all the history was cleared.
        expected_4 = exists(history_empty_pattern.similar(0.9), 10)
        assert_true(self, expected_4, 'All the history was cleared successfully.')
