# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Tracking Protection can be successfully deactivated for both private and normal browsing sessions',
        test_case_id='103330',
        test_suite_id='1826',
        locales=['en-US'],
        blocked_by={'id': 'issue_402', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        tracking_protection_shield_pattern = LocationBar.TRACKING_PROTECTION_SHIELD_ACTIVATED
        privacy_page_pattern = AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED
        cnn_logo_pattern = LocalWeb.CNN_LOGO
        custom_privacy_radio_pattern = Pattern('custom_privacy_radio.png')
        trackers_checked_pattern = Pattern('trackers_checked.png')
        trackers_unchecked_pattern = Pattern('trackers_unchecked.png')
        cookies_checked_pattern = Pattern('cookies_preference_checked.png')
        cookies_unchecked_pattern = Pattern('cookies_preference_unchecked.png')
        private_browsing_tab_pattern = Pattern('private_browsing_tab_logo.png')
        private_content_blocking_warning_pattern = Pattern('private_window_content_blocking_warning.png')
        info_button_pattern = Pattern('info_button.png')
        trackers_button_pattern = Pattern('trackers_button.png')
        trackers_popup_title_pattern = Pattern('trackers_popup_title.png')
        blocked_tracker_pattern = Pattern('blocked_tracker_label.png')
        trackers_icon_pattern = Pattern('trackers_icon.png')
        to_block_set_to_strict_pattern = Pattern('to_block_set_to_strict.png')

        new_tab()

        navigate('about:preferences#privacy')

        navigated_to_preferences = exists(privacy_page_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert navigated_to_preferences is True, 'The about:preferences#privacy page is successfully displayed.'

        move(Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2))

        custom_radio_found = scroll_until_pattern_found(custom_privacy_radio_pattern, scroll_down, (25,), 20, 1)
        assert custom_radio_found is True, '"Custom" radio button from the "Content Blocking" section is displayed.'

        click(custom_privacy_radio_pattern)

        custom_protection_popup_opened = exists(trackers_checked_pattern)
        assert custom_protection_popup_opened is True, 'The Custom panel is displayed.'

        click(trackers_checked_pattern, 1)

        content_blocking_trackers_unchecked = exists(trackers_unchecked_pattern)
        assert content_blocking_trackers_unchecked is True, 'The trackers checkbox is unchecked successfully.'

        click(cookies_checked_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        content_blocking_cookies_unchecked = exists(cookies_unchecked_pattern)
        assert content_blocking_cookies_unchecked is True, 'The cookies checkbox is unchecked successfully.'

        close_tab()

        new_tab()

        navigate('http://edition.cnn.com')

        cnn_logo_exists = exists(cnn_logo_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert cnn_logo_exists is True, 'The website is successfully displayed.'

        tracking_protection_shield_common_window = exists(tracking_protection_shield_pattern,
                                                          FirefoxSettings.FIREFOX_TIMEOUT)
        assert tracking_protection_shield_common_window is False, 'The Content blocking shield' \
                                                                  ' is not displayed near the address bar.'

        new_private_window()

        private_window_opened = exists(private_browsing_tab_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert private_window_opened is True, 'Private browsing window opened'

        content_blocking_private_displayed = exists(private_content_blocking_warning_pattern,
                                                    FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert content_blocking_private_displayed is False, '"Some websites use trackers' \
                                                            ' that can monitor your activity" etc. not displayed'

        navigate('http://edition.cnn.com')

        cnn_logo_exists = exists(cnn_logo_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert cnn_logo_exists is True, 'The website is successfully displayed.'

        tracking_protection_shield_private_window = exists(tracking_protection_shield_pattern,
                                                           FirefoxSettings.FIREFOX_TIMEOUT)
        assert tracking_protection_shield_private_window is False, 'The Content blocking shield' \
                                                                   ' is not displayed near the address bar'

        info_button_located = exists(info_button_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert info_button_located is True, 'The "i button" (Info button) is located near the address bar'

        click(info_button_pattern)

        open_trackers_list_button_located = exists(trackers_button_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert open_trackers_list_button_located is True, 'The site information panel is displayed.'

        click(trackers_button_pattern)

        trackers_popup_displayed = exists(trackers_popup_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert trackers_popup_displayed is True, 'Trackers popup window is displayed on screen'

        list_of_active_trackers_displayed = exists(trackers_icon_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert list_of_active_trackers_displayed is True, 'A list of active trackers is successfully displayed.'

        trackers_blocked = exists(blocked_tracker_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert trackers_blocked is False, 'The trackers are not blocked.'

        to_block_set_to_strict_located = exists(to_block_set_to_strict_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert to_block_set_to_strict_located is True, '\'To block all trackers, set content' \
                                                       ' blocking to "Strict"\' is displayed'

        close_window()
