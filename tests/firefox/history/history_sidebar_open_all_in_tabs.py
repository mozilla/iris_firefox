# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This is a test for the \'Open All in Tabs\' option from the History sidebar.',
        locale=['en-US'],
        test_case_id='120117',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        firefox_privacy_logo_pattern = Pattern('firefox_privacy_logo.png')
        search_history_box_pattern = Sidebar.HistorySidebar.SEARCH_BOX
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        iris_logo_pattern = Pattern('iris_logo_tab.png')
        mozilla_logo_pattern = Pattern('mozilla_logo_tab.png')

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

        expected_4 = exists(history_today_sidebar_pattern, 10)
        assert expected_4 is True, 'Expand history button displayed properly.'

        # 'Open All in Tabs' from the context menu.
        right_click(history_today_sidebar_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        type(text='o')

        # Check that all the pages loaded successfully.
        expected_5 = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected_5 is True, 'Firefox page loaded successfully.'

        next_tab()

        expected_6 = exists(firefox_privacy_logo_pattern, 10)
        assert expected_6 is True, 'Firefox Privacy Notice loaded successfully.'

        expected_7 = exists(iris_logo_pattern, 10)
        assert expected_7 is True, 'Iris local page loaded successfully.'

        expected_8 = exists(mozilla_logo_pattern, 10)
        assert expected_8 is True, 'Mozilla page loaded successfully.'
