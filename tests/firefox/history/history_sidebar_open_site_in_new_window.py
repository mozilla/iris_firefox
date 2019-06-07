# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This is a test that opens a page from the History sidebar using the \'Open in a New Window\' ' \
                    'button from the context menu.',
        locale=['en-US'],
        test_case_id='120121',
        test_suite_id='2000'
    )
    def run(self, firefox):
        history_sidebar_mozilla = LocalWeb.MOZILLA_BOOKMARK_SMALL
        search_history_box_pattern = Sidebar.HistorySidebar.SEARCH_BOX
        sidebar_history_today_pattern = Sidebar.HistorySidebar.Timeline.TODAY

        left_upper_corner = Screen().new_region(0, 0, Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT / 2)

        # Open some pages to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_1 is True, 'Mozilla page loaded successfully.'

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        expected_2 = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected_2 is True, 'Firefox page loaded successfully.'

        # Open the History sidebar.
        history_sidebar()

        expected_3 = exists(search_history_box_pattern, 10)
        assert expected_3 is True, 'Sidebar was opened successfully.'

        expected_4 = exists(sidebar_history_today_pattern, 10)
        assert expected_4 is True, 'Expand history button displayed properly.'

        click(sidebar_history_today_pattern)

        # Open a page from the History sidebar using the 'Open in a New Window' button from the context menu.

        expected_5 = left_upper_corner.exists(history_sidebar_mozilla.similar(0.7), 10)
        assert expected_5 is True, 'Mozilla page is displayed in the History list successfully.'

        right_click(history_sidebar_mozilla.similar(0.7), 1)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        type(text='n')

        expected_6 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_6 is True, 'Mozilla page loaded successfully.'
