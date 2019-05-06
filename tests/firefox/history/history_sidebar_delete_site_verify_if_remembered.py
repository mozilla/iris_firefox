# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Delete a page from the History sidebar and verify it is still remembered in the URL bar.',
        locale='[en-US]',
        test_case_id='120131',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        search_history_box = Sidebar.HistorySidebar.SEARCH_BOX
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        local_server_autocomplete = Pattern('local_server_autocomplete.png')
        mozilla_bookmark_small_pattern = LocalWeb.MOZILLA_BOOKMARK_SMALL

        left_upper_corner = Screen().new_region(0, 0, Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT / 2)

        # Open some pages to create some history.
        close_tab()
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_1, 'Mozilla page loaded successfully.'

        close_tab()

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        expected_2 = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected_2, 'Firefox page loaded successfully.'

        close_tab()
        new_tab()

        # Open the History sidebar.
        history_sidebar()

        expected_3 = exists(search_history_box, 10)
        assert expected_3, 'Sidebar was opened successfully.'

        expected_4 = exists(history_today_sidebar_pattern, 10)
        assert expected_4, 'Expand history button displayed properly.'

        click(history_today_sidebar_pattern)

        # Delete a page from the History sidebar.
        expected_5 = left_upper_corner.exists(mozilla_bookmark_small_pattern.similar(0.7), 10)
        assert expected_5, 'Mozilla page is displayed in the History list successfully.'

        right_click_and_type(mozilla_bookmark_small_pattern,keyboard_action='d')


        try:
            expected_6 = left_upper_corner.wait_vanish(mozilla_bookmark_small_pattern, 10)
            assert expected_6, 'Mozilla page was deleted successfully from the history.'
        except FindError:
            raise FindError('Mozilla page is still displayed in the history.')

        # Check that Mozilla page is not displayed in the Recent History list.
        open_library_menu('History')

        expected_7 = wait_vanish(mozilla_bookmark_small_pattern.similar(0.9), 10)
        assert expected_7, 'Mozilla page is not displayed in the Recent History list.'

        type(Key.ESC)

        # Check that the local server is still auto-completed in the URL bar.
        select_location_bar()
        paste('127')

        expected_8 = exists(local_server_autocomplete, 10)
        assert expected_8, 'Local server is auto-completed successfully.'
