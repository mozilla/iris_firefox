# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Clear Recent History from a predefined time range.'

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.LIKE_NEW
        return

    def run(self):
        clear_recent_history_window = 'clear_recent_history_window.png'
        history_items_old = 'history_items_old.png'
        history_items_today = 'expand_button_history_sidebar.png'
        clear_recent_history_last_hour = 'clear_recent_history_last_hour.png'

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

        # Open the Clear Recent History window and select 'Today'.
        clear_recent_history()
        expected_3 = exists(clear_recent_history_window, 10)
        assert_true(self, expected_3, 'Clear Recent History window was displayed properly.')

        if Settings.is_mac():
            click(clear_recent_history_last_hour)
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

        # Check that 'Today' was removed from the History sidebar.
        try:
            expected_4 = wait_vanish(history_items_today, 10)
            assert_true(self, expected_4, 'Today\'s history was removed successfully.')
        except FindError:
            raise FindError('Today\'s history is still present.')

        expected_5 = exists(Pattern(history_items_old).similar(0.9), 10)
        assert_true(self, expected_5, 'Old history is still displayed properly.')
