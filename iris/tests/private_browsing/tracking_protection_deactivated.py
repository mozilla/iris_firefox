# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Tracking Protection can be successfully deactivated for both private and normal browsing sessions'
        self.test_case_id = '103330'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def run(self):
        tracking_protection_shield_pattern = LocationBar.TRACKING_PROTECTION_SHIELD_ACTIVATED
        privacy_page_pattern = AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED
        cnn_logo_pattern = LocalWeb.CNN_LOGO
        custom_privacy_radio_pattern = Pattern('custom_privacy_radio.png')
        trackers_checked_pattern = Pattern('trackers_checked.png')
        trackers_unchecked_pattern = Pattern('trackers_unchecked.png')
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

        navigated_to_preferences = exists(privacy_page_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, navigated_to_preferences, 'The about:preferences#privacy page is successfully displayed.')

        custom_radio_found = exists(custom_privacy_radio_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, custom_radio_found, 'Custom" radio button from the "Content Blocking" section is displayed.')

        click(custom_privacy_radio_pattern, 1)

        custom_protection_popup_opened = exists(trackers_checked_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, custom_protection_popup_opened, 'The Custom panel is displayed.')

        click(trackers_checked_pattern)

        content_blocking_trackers_unchecked = exists(trackers_unchecked_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, content_blocking_trackers_unchecked, 'The trackers checkbox is unchecked successfully.')

        content_blocking_cookies_unchecked = exists(cookies_unchecked_pattern)
        assert_true(self, content_blocking_cookies_unchecked, 'The cookies checkbox is unchecked successfully.')

        close_tab()

        new_tab()

        navigate('http://edition.cnn.com')

        cnn_logo_exists = exists(cnn_logo_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cnn_logo_exists, 'The website is successfully displayed.')

        tracking_protection_shield_common_window = exists(tracking_protection_shield_pattern,
                                                          Settings.SHORT_FIREFOX_TIMEOUT)
        assert_false(self, tracking_protection_shield_common_window,
                     'The Content blocking shield is not displayed near the address bar.')

        new_private_window()

        private_window_opened = exists(private_browsing_tab_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, private_window_opened, 'Private browsing window opened')

        content_blocking_private_displayed = exists(private_content_blocking_warning_pattern,
                                                    Settings.SHORT_FIREFOX_TIMEOUT)
        assert_false(self, content_blocking_private_displayed,
                     '"Some websites use trackers that can monitor your activity" etc. not displayed')

        navigate('http://edition.cnn.com')

        cnn_logo_exists = exists(cnn_logo_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cnn_logo_exists, 'The website is successfully displayed.')

        tracking_protection_shield_private_window = exists(tracking_protection_shield_pattern,
                                                           Settings.SHORT_FIREFOX_TIMEOUT)
        assert_false(self, tracking_protection_shield_private_window,
                     'The Content blocking shield is not displayed near the address bar')

        info_button_located = exists(info_button_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, info_button_located, 'The "i button" (Info button) is located near the address bar')

        click(info_button_pattern)

        open_trackers_list_button_located = exists(trackers_button_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, open_trackers_list_button_located, 'The site information panel is displayed.')

        click(trackers_button_pattern)

        trackers_popup_displayed = exists(trackers_popup_title_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, trackers_popup_displayed, 'Trackers popup window is displayed on screen')

        list_of_active_trackers_displayed = exists(trackers_icon_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, list_of_active_trackers_displayed, 'A list of active trackers is successfully displayed.')

        trackers_blocked = exists(blocked_tracker_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_false(self, trackers_blocked, 'The trackers are not blocked.')

        to_block_set_to_strict_located = exists(to_block_set_to_strict_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, to_block_set_to_strict_located,
                    '\'To block all trackers, set content blocking to "Strict"\' is displayed')

        close_window()
