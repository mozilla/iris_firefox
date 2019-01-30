# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Tracking Protection can be turned off for individual sites'
        self.test_case_id = '107431'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def run(self):
        tracking_protection_shield_pattern = LocationBar.TRACKING_PROTECTION_SHIELD_ACTIVATED
        tracking_protection_shield_deactivated_pattern = LocationBar.TRACKING_PROTECTION_SHIELD_DEACTIVATED

        cnn_site_logo_pattern = Pattern('cnn_logo.png')
        cnn_blocked_content_pattern = Pattern('cnn_blocked_content.png')
        disable_blocking_button_pattern = Pattern('turn_off_blocking_for_site_button.png')
        enable_blocking_button_pattern = Pattern('turn_on_blocking_for_site_button.png')
        tracking_content_detected_message_pattern = Pattern('tracking_content_detected_message.png')
        tracking_attempts_blocked_message_pattern = Pattern('tracking_attempts_blocked_message.png')

        # Open a new Private window tab.
        new_private_window()
        private_browsing_tab_logo_displayed = exists(PrivateWindow.private_window_pattern, 5)
        assert_true(self, private_browsing_tab_logo_displayed, "New private window is displayed")

        # Access the website.
        navigate("https://edition.cnn.com")
        website_displayed = exists(cnn_site_logo_pattern, 30)
        assert_true(self, website_displayed, 'The website is successfully displayed')

        restore_firefox_focus()
        repeat_key_down(10)

        tracking_protection_shield_displayed = exists(tracking_protection_shield_pattern, 5)
        assert_true(self, tracking_protection_shield_displayed, 'The tracking protection shield is displayed')

        cnn_blocked_content_displayed = exists(cnn_blocked_content_pattern, 30)
        assert_false(self, cnn_blocked_content_displayed,
                     'Websites content that contain tracking elements are not displayed on the page')

        # Click the tracking protection shield icon

        click(tracking_protection_shield_pattern)
        disable_blocking_button_displayed = exists(disable_blocking_button_pattern, 5)
        assert_true(self, disable_blocking_button_displayed, 'The site information panel is displayed')

        # Click the "Disable protection for this session" option
        click(disable_blocking_button_pattern)
        website_displayed = exists(cnn_site_logo_pattern, 60)
        assert_true(self, website_displayed, 'The website successfully refreshes')

        tracking_protection_shield_deactivated_displayed = exists(tracking_protection_shield_deactivated_pattern, 5)
        assert_true(self, tracking_protection_shield_deactivated_displayed,
                    'The tracking protection shield is displayed as deactivated')

        mouse_move(tracking_protection_shield_deactivated_pattern)

        tracking_content_detected_message_displayed = exists(tracking_content_detected_message_pattern, 5)
        assert_true(self, tracking_content_detected_message_displayed,
                    'The tracking protection shield displays a "Tracking content detected" tooltip message')

        cnn_blocked_content_displayed = exists(cnn_blocked_content_pattern, 30)
        assert_true(self, cnn_blocked_content_displayed,
                    'Websites content that contain tracking elements are displayed on the page')

        # Click the tracking protection shield icon
        click(tracking_protection_shield_deactivated_pattern)
        enable_blocking_button_displayed = exists(enable_blocking_button_pattern, 5)
        assert_true(self, enable_blocking_button_displayed, 'The site information panel is displayed')

        # Click the "Enable protection" option
        click(enable_blocking_button_pattern)
        website_displayed = exists(cnn_site_logo_pattern, 30)
        assert_true(self, website_displayed, 'The website successfully refreshes')

        tracking_protection_shield_displayed = exists(tracking_protection_shield_pattern, 5)
        assert_true(self, tracking_protection_shield_displayed,
                    'The tracking protection shield is displayed as activated')

        mouse_move(tracking_protection_shield_pattern)
        tracking_attempts_blocked_message_displayed = exists(tracking_attempts_blocked_message_pattern, 5)
        assert_true(self, tracking_attempts_blocked_message_displayed,
                    'The tracking protection shield displays a "Tracking attempts blocked" tooltip message')

        cnn_blocked_content_displayed = exists(cnn_blocked_content_pattern, 30)
        assert_false(self, cnn_blocked_content_displayed,
                     'Websites content that contain tracking elements are not displayed on the page')
        close_window()
