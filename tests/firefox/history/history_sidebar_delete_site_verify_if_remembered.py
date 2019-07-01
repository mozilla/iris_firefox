# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Delete a page from the History sidebar and verify it is still remembered in the URL bar.',
        locale=['en-US'],
        test_case_id='120131',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        search_history_box_pattern = Sidebar.HistorySidebar.SEARCH_BOX
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        local_server_autocomplete_pattern = Pattern('local_server_autocomplete.png')
        mozilla_bookmark_small_pattern = LocalWeb.MOZILLA_BOOKMARK_SMALL

        left_upper_corner = Screen().new_region(0, 0, Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT / 2)

        # Open some pages to create some history.
        close_tab()
        new_tab()

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_logo_exists = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_logo_exists, 'Mozilla page loaded successfully.'

        close_tab()
        new_tab()

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        firefox_logo_exists = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert firefox_logo_exists, 'Firefox page loaded successfully.'

        close_tab()
        new_tab()

        # Open the History sidebar.
        history_sidebar()

        search_history_box_exists = exists(search_history_box_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert search_history_box_exists, 'Sidebar was opened successfully.'

        history_today_sidebar_exists = exists(history_today_sidebar_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert history_today_sidebar_exists, 'Expand history button displayed properly.'

        click(history_today_sidebar_pattern)

        # Delete a page from the History sidebar.
        mozilla_bookmark_small_exists = left_upper_corner.exists(mozilla_bookmark_small_pattern.similar(0.7),
                                                                 FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_bookmark_small_exists, 'Mozilla page is displayed in the History list successfully.'

        right_click_and_type(mozilla_bookmark_small_pattern, keyboard_action='d')

        try:
            mozilla_bookmark_small_vanished = left_upper_corner.wait_vanish(mozilla_bookmark_small_pattern,
                                                                            FirefoxSettings.FIREFOX_TIMEOUT)
            assert mozilla_bookmark_small_vanished, 'Mozilla page was deleted successfully from the history.'
        except FindError:
            raise FindError('Mozilla page is still displayed in the history.')

        # Check that Mozilla page is not displayed in the Recent History list.
        open_library_menu('History')

        mozilla_bookmark_small_exists = exists(mozilla_bookmark_small_pattern.similar(0.9),
                                               FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_bookmark_small_exists is False, 'Mozilla page is not displayed in the Recent History list.'

        type(Key.ESC)

        # Check that the local server is still auto-completed in the URL bar.
        select_location_bar()
        type('127')

        local_server_autocomplete_exists = exists(local_server_autocomplete_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert local_server_autocomplete_exists, 'Local server is auto-completed successfully.'
