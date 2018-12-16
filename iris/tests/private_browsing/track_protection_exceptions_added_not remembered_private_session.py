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
        cnn_site_logo_pattern = LocalWeb.CNN_LOGO

        # Access the website
        navigate('https://edition.cnn.com')

        website_displayed = exists(cnn_site_logo_pattern, 30)
        assert_true(self, website_displayed, 'The Website is successfully displayed')

        tracking_protection_shield_displayed = exists(tracking_protection_shield_pattern, 10)
        assert_true(self, tracking_protection_shield_displayed,
                    'The Tracking Protection shield is displayed near the address bar')

        # Click the tracking protection shield icon
        click(tracking_protection_shield_pattern)
        disable_blocking_button_displayed = exists(SiteInformationPanel.DISABLE_BLOCKING_BUTTON, 5)
        assert_true(self, disable_blocking_button_displayed, 'The site information panel is displayed')

        # Click the "Disable protection for this session" option
        click(SiteInformationPanel.DISABLE_BLOCKING_BUTTON)
        website_displayed = exists(cnn_site_logo_pattern, 30)
        assert_true(self, website_displayed, 'The website successfully refreshes')

        tracking_protection_shield_deactivated_displayed = exists(LocationBar.TRACKING_PROTECTION_SHIELD_DEACTIVATED, 5)
        assert_true(self, tracking_protection_shield_deactivated_displayed,
                    'The tracking protection shield is displayed as deactivated')

        mouse_move(LocationBar.TRACKING_PROTECTION_SHIELD_DEACTIVATED)

        tracking_content_detected_message_displayed = exists(LocationBar.TRACKING_CONTENT_DETECTED_MESSAGE, 5)
        assert_true(self, tracking_content_detected_message_displayed,
                    'The tracking protection shield displays a "Tracking content detected" tooltip message')

        cnn_blocked_content_displayed = exists(LocalWeb.CNN_BLOCKED_CONTENT_ADV, 30)
        assert_true(self, cnn_blocked_content_displayed,
                    'Websites content that contain tracking elements are displayed on the page')

        #  Access the about:preferences#privacy page.
        new_tab()
        navigate('about:preferences#privacy')

        privacy_prefs_page_displayed = exists(LocalWeb.ABOUT_PREFERENCES_PRIVACY_ADDRESS, 20)
        assert_true(self, privacy_prefs_page_displayed, "The privacy preferences page is successfully displayed")

        #  Click the "Exceptions" button from the Tracking protection section.
        click(AboutPreferences.Privacy.TRACKING_PROTECTION_EXCEPTIONS_BUTTON)

        previously_accessed_site_displayed = exists(LocalWeb.CNN_CONTENT_BLOCKING_EXCEPTION)
        assert_false(self, previously_accessed_site_displayed,
                     "The previously accessed website is not displayed "
                     "inside the Tracking Protection exceptions panel.")


