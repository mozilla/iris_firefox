# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This is a test that opens a page from the History sidebar using the \'Open in a New Private ' \
                    'Window\' button from the context menu.',
        locale=['en-US'],
        test_case_id='120122',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        search_history_box_pattern = Sidebar.HistorySidebar.SEARCH_BOX
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY

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

        history_today_location = find(history_today_sidebar_pattern)
        history_today_width, history_today_height = history_today_sidebar_pattern.get_size()
        history_sidebar_region = Region(0, history_today_location.y, history_today_width * 3, history_today_height * 10)

        click(history_today_sidebar_pattern)

        # Open a page from the History sidebar using the 'Open in a New Private Window' button from the context menu.

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        expected_5 = history_sidebar_region.exists('Mozilla', 10)
        assert expected_5 is True, 'Mozilla page is displayed in the History list successfully.'

        right_click('Mozilla', 1, region=history_sidebar_region)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        type(text='p')

        expected_6 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_6 is True, 'Mozilla page loaded successfully.'
