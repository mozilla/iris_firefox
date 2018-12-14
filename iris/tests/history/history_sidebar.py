# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open the History sidebar.'
        self.test_case_id = '118811'
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
        search_history_box_pattern = Sidebar.HistorySidebar.SEARCH_BOX
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        history_sidebar_default_pattern = Pattern('history_sidebar_default.png')

        # Open the History sidebar.
        history_sidebar()
        expected_1 = exists(search_history_box_pattern, 10)
        assert_true(self, expected_1, 'Sidebar was opened successfully.')
        expected_2 = exists(history_today_sidebar_pattern, 10)
        assert_true(self, expected_2, 'Expand history button displayed properly.')
        click(history_today_sidebar_pattern)

        # Check the default items are displayed.
        expected_3 = exists(history_sidebar_default_pattern, 10)
        assert_true(self, expected_3, 'The expected items are displayed in the History list.')
