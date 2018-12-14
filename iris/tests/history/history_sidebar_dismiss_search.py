# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Dismiss the search from the History sidebar.'
        self.test_case_id = '119442'
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
        history_sidebar_focus_pattern = Pattern('history_sidebar_focus.png')
        search_history_box_pattern = Sidebar.HistorySidebar.SEARCH_BOX
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        x_button_search_history_box_pattern = Sidebar.SidebarHeader.CLEAR_SEARCH_BOX
        history_sidebar_items_pattern = Pattern('history_sidebar_items.png')

        # Open a page to create some history.
        navigate(LocalWeb.FOCUS_TEST_SITE)
        expected_1 = exists(LocalWeb.FOCUS_LOGO, 10)
        assert_true(self, expected_1, 'Focus page loaded successfully.')

        # Open the History sidebar.
        history_sidebar()
        expected_2 = exists(search_history_box_pattern, 10)
        assert_true(self, expected_2, 'Sidebar was opened successfully.')
        expected_3 = exists(history_today_sidebar_pattern, 10)
        assert_true(self, expected_3, 'Expand history button displayed properly.')
        click(history_today_sidebar_pattern)
        click(search_history_box_pattern)

        # Check that Focus page is found in the History list.
        paste('focus')
        type(Key.TAB)
        expected_4 = exists(history_sidebar_focus_pattern, 10)
        assert_true(self, expected_4, 'Focus page was found in the History list successfully.')

        # Clear the History search box.
        expected_5 = exists(x_button_search_history_box_pattern, 10)
        assert_true(self, expected_5, 'Clear field button was displayed properly.')
        click(x_button_search_history_box_pattern)
        expected_6 = exists(history_sidebar_items_pattern, 10)
        expected_7 = exists(search_history_box_pattern, 10)
        assert_true(self, expected_6 and expected_7, 'The expected items are displayed in the History list.')
