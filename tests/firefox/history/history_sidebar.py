# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open the History sidebar.',
        locale=['en-US'],
        test_case_id='118811',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        search_history_box_pattern = Sidebar.HistorySidebar.SEARCH_BOX
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        history_sidebar_default_pattern = Pattern('history_sidebar_default.png')

        # Open the History sidebar.
        history_sidebar()

        expected_1 = exists(search_history_box_pattern, 10)
        assert expected_1, 'Sidebar was opened successfully.'
        
        expected_2 = exists(history_today_sidebar_pattern, 10)
        assert expected_2, 'Expand history button displayed properly.'

        click(history_today_sidebar_pattern)

        # Check the default items are displayed.
        expected_3 = exists(history_sidebar_default_pattern, 10)
        assert expected_3, 'The expected items are displayed in the History list.'
