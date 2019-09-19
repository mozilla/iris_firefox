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

        expected_3 = exists(search_history_box_pattern, 10)
        assert expected_3 is True, 'Sidebar was opened successfully.'

        expected_4 = exists(history_today_sidebar_pattern, 10)
        assert expected_4 is True, 'Expand history button displayed properly.'

        history_today_location = find(history_today_sidebar_pattern)
        history_today_width, history_today_height = history_today_sidebar_pattern.get_size()
        history_sidebar_region = Region(0, history_today_location.y, history_today_width * 3, history_today_height * 10)

        click(history_today_sidebar_pattern)

        # Copy a website from the History sidebar and paste it into the URL bar.
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        expected_4 = exists('Mozilla', 10, history_sidebar_region)
        assert expected_4, 'Mozilla page is displayed in the History list successfully.'

        right_click('Mozilla', region=history_sidebar_region)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        type('c')

        select_location_bar()
        edit_paste()
        type(Key.ENTER)

        # Check that the page was opened successfully.
        expected_5 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_5, 'Mozilla page loaded successfully.'
