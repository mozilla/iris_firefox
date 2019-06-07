# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Copy a website from the History sidebar and paste it into the URL bar.',
        locale=['en-US'],
        test_case_id='120129',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        search_history_box_pattern = Sidebar.HistorySidebar.SEARCH_BOX
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY

        # Open a page to create some history.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_1, 'Mozilla page loaded successfully.'

        close_tab()

        # Open the History sidebar.
        history_sidebar()

        expected_2 = exists(search_history_box_pattern, 10)
        assert expected_2, 'Sidebar was opened successfully.'

        expected_3 = exists(history_today_sidebar_pattern, 10)
        assert expected_3, 'Expand history button displayed properly.'

        click(history_today_sidebar_pattern)

        # Copy a website from the History sidebar and paste it into the URL bar.
        expected_4 = exists(LocalWeb.MOZILLA_BOOKMARK_SMALL, 10)
        assert expected_4, 'Mozilla page is displayed in the History list successfully.'

        right_click_and_type(LocalWeb.MOZILLA_BOOKMARK_SMALL, keyboard_action='c')


        select_location_bar()
        edit_paste()
        type(Key.ENTER)

        # Check that the page was opened successfully.
        expected_5 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_5, 'Mozilla page loaded successfully.'
