# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Tracking Protection is blocking eligible content',
        test_case_id='3956',
        test_suite_id='69',
        locale=['en-US'],
    )
    def run(self, firefox):
        disconnect_page_logo_pattern = Pattern('disconnect_page_logo.png')
        its_a_tracker_tab_label_pattern = Pattern('its_a_tracker_tab_label.png')
        if not OSHelper.is_mac():
            blocked_tests_area_pattern = Pattern('blocked_tests_area.png').similar(.95)
        else:
            blocked_tests_area_pattern = Pattern('blocked_tests_area.png')
        protection_list_downloading_time = 60

        navigate('https://disconnect.me/')

        disconnect_page_loaded = exists(disconnect_page_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert disconnect_page_loaded, 'Disconnect.me page loaded'

        # Wait around 30 sec - 1 minute until Firefox automatically downloads the Tracking Protection basic
        # protection list from disconnect.me.

        time.sleep(protection_list_downloading_time)

        new_private_window()

        private_window_opened = exists(PrivateWindow.private_window_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert private_window_opened, 'A new private window is successfully opened.'

        navigate('https://itisatrap.org/firefox/its-a-tracker.html')

        its_a_tracker_page_loaded = exists(its_a_tracker_tab_label_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert its_a_tracker_page_loaded, 'https://itisatrap.org/firefox/its-a-tracker.html page loaded'

        blocked_tests_area_displayed = exists(blocked_tests_area_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert blocked_tests_area_displayed, 'Blocked tests area displayed'

        blocked_tests_location = find(blocked_tests_area_pattern)
        blocked_tests_area_width, blocked_tests_area_height = blocked_tests_area_pattern.get_size()
        blocked_tests_region = Region(blocked_tests_location.x, blocked_tests_location.y, blocked_tests_area_width,
                                      blocked_tests_area_height)

        blocked_tests = ['a simulated third-party tracker was correctly blocked',
                         'a simulated first-party tracker was correctly loaded',
                         'the DNT signal was correctly sent']

        blocked_test_find = 0
        tests_are_blocked = False

        for test in blocked_tests:
            test_is_blocked = exists(test, FirefoxSettings.FIREFOX_TIMEOUT, blocked_tests_region)
            if test_is_blocked:
                blocked_test_find += 1

        if blocked_test_find == 3:
            tests_are_blocked = True

        assert tests_are_blocked, 'All tests are correctly blocked (green)'

        new_tab()

        navigate('https://edition.cnn.com/')

        cnn_page_opened = exists(LocalWeb.CNN_LOGO, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert cnn_page_opened, 'The CNN site successfully opened'

        tracking_protection_shield_displayed = exists(LocationBar.TRACKING_PROTECTION_SHIELD_ACTIVATED,
                                                      FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert tracking_protection_shield_displayed, 'The tracking protection shield is displayed in the URL bar.'

        close_window()
