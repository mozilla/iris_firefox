# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Tracking protection exceptions can be added ' \
                    'but can\'t be remembered using private browsing session'
        self.test_case_id = '107718'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def run(self):
        tracking_protection_shield_pattern = LocationBar.TRACKING_PROTECTION_SHIELD_ACTIVATED
        tracking_protection_shield_deactivated_pattern = LocationBar.TRACKING_PROTECTION_SHIELD_DEACTIVATED
        tracking_content_detected_pattern = LocationBar.TRACKING_CONTENT_DETECTED_MESSAGE
        cnn_logo_pattern = LocalWeb.CNN_LOGO
        # Access the website
        blocking_turn_off_pattern = Pattern("blocking_turn_off.png")
        empty_exc_list_pattern = Pattern("empty_exc_list.png")
        manage_exceptions_button_pattern = Pattern("manage_exceptions_button.png")
        private_browsing_tab_logo_pattern = Pattern("private_browsing_tab_logo.png")

        new_private_window()
        private_window_opened = exists(private_browsing_tab_logo_pattern)
        assert_true(self, private_window_opened,
                    "Private window opened")

        navigate("https://edition.cnn.com/?refresh=1")

        page_loaded = exists(cnn_logo_pattern, timeout=30)
        assert_true(self, page_loaded,
                    "The website is successfully displayed. ")

        tracking_protection_shield_displayed = exists(tracking_protection_shield_pattern,
                                                      timeout=5)
        assert_true(self, tracking_protection_shield_displayed,
                    "Tracking protection shield displayed")

        cnn_blocked_content_not_displayed = not exists(LocalWeb.CNN_BLOCKED_CONTENT_ADV, 5)
        assert_true(self, cnn_blocked_content_not_displayed,
                    'Websites content that contain tracking elements are not displayed on the page')

        shield_button = find(tracking_protection_shield_pattern)
        click(shield_button)

        protection_popup_opened = exists(blocking_turn_off_pattern, 20)
        assert_true(self, protection_popup_opened,
                    "The site information panel is displayed.")

        click(blocking_turn_off_pattern)

        tracking_protection_shield_deactivated_exists = exists(tracking_protection_shield_deactivated_pattern, 40)
        assert_true(self, tracking_protection_shield_deactivated_exists,
                    'The tracking protection shield is displayed as deactivated (red strikethrough).')

        page_loaded = exists(cnn_logo_pattern, 30)
        assert_true(self, page_loaded,
                    "The website is loaded.")

        click_location = Location(x=0, y=300)
        click(click_location, 0.2)
        type(Key.PAGE_DOWN)

        cnn_blocked_content_displayed = exists(LocalWeb.CNN_BLOCKED_CONTENT_ADV, 30)
        assert_true(self, cnn_blocked_content_displayed,
                    'Websites content that contain tracking elements are displayed on the page')

        hover(tracking_protection_shield_deactivated_pattern, 40)
        tracking_content_detected_exists = exists(tracking_content_detected_pattern, 40)
        assert_true(self, tracking_content_detected_exists,
                    'On hover, the tracking protection shield displays a "Tracking content detected" tooltip message.')

        close_window()

        new_tab()
        navigate("about:preferences#privacy")
        privacy_prefs_opened = exists(manage_exceptions_button_pattern)
        assert_true(self, privacy_prefs_opened,
                    "The about:preferences#privacy page is successfully displayed.")

        manage_exceptions_button = find(manage_exceptions_button_pattern)
        click(manage_exceptions_button)
        exceptions_window_opened = exists(empty_exc_list_pattern)
        assert_true(self, exceptions_window_opened,
                    "The previously accessed website is not displayed inside the Tracking Protection exceptions panel.")
