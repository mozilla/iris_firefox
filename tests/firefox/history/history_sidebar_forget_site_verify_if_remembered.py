# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Forget a page from the History sidebar and verify it is not remembered in the URL bar.',
        locale=['en-US'],
        test_case_id='120133',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        search_history_box_pattern = Sidebar.HistorySidebar.SEARCH_BOX
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        local_server_autocomplete_pattern = Pattern('local_server_autocomplete.png')

        # Open some pages to create some history.
        close_tab()
        new_tab()

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected_1 = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected_1 is True, 'Mozilla page loaded successfully.'

        close_tab()

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        expected_2 = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected_2 is True, 'Firefox page loaded successfully.'

        close_tab()
        new_tab()

        # Open the History sidebar.
        history_sidebar()

        expected_3 = exists(search_history_box_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected_3 is True, 'Sidebar was opened successfully.'

        expected_4 = exists(history_today_sidebar_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected_4 is True, 'Expand history button displayed properly.'

        history_today_location = find(history_today_sidebar_pattern)
        history_today_width, history_today_height = history_today_sidebar_pattern.get_size()
        history_sidebar_region = Region(0, history_today_location.y, history_today_width * 3, history_today_height * 10)

        click(history_today_sidebar_pattern)

        # Forget a page from the History sidebar.

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        expected_5 = history_sidebar_region.exists('Mozilla', FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected_5 is True, 'Mozilla page is displayed in the History list successfully.'

        right_click('Mozilla', region=history_sidebar_region)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        type('f')

        try:
            expected_6 = history_sidebar_region.exists('Mozilla', FirefoxSettings.FIREFOX_TIMEOUT)
            assert expected_6 is not True, 'Mozilla page was deleted successfully from the history.'
        except FindError:
            raise FindError('Mozilla page is still displayed in the history.')

        # Check that Mozilla page is not displayed in the Recent History list.
        open_library_menu('History')

        expected_7 = exists('Mozilla', FirefoxSettings.FIREFOX_TIMEOUT, history_sidebar_region)
        assert expected_7 is not True, 'Mozilla page is not displayed in the Recent History list.'

        type(Key.ESC)

        # Check that the local server is not auto-completed in the URL bar.
        select_location_bar()
        type('127')

        expected_8 = exists(local_server_autocomplete_pattern.similar(0.9), FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected_8 is not True, 'Local server is not auto-completed in the URL bar.'
