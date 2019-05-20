# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Search in History sidebar for an unavailable website.',
        locale=['en-US'],
        test_case_id='119441',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        search_history_box_pattern = Sidebar.HistorySidebar.SEARCH_BOX
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        history_search_no_results_pattern = Pattern('history_search_no_results.png')

        # Open a page to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_1 is True, 'Mozilla page loaded successfully.'

        # Open the History sidebar.
        history_sidebar()

        expected_2 = exists(search_history_box_pattern, 10)
        assert expected_2 is True, 'Sidebar was opened successfully.'

        expected_3 = exists(history_today_sidebar_pattern, 10)
        assert expected_3 is True, 'Expand history button displayed properly.'

        click(history_today_sidebar_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        click(search_history_box_pattern)

        # Check that an unavailable page is not found in the History list.
        paste('test')
        type(Key.TAB)

        expected_4 = exists(history_search_no_results_pattern, 10)
        assert expected_4 is True, 'The page wasn\'t found in the History list.'
