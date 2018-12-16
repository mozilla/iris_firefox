# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Tracking protection exceptions can be successfully added,' \
                    'remembered and removed from normal browsing session'
        self.test_case_id = '107717'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def run(self):
        always_block_trackers_not_selected_pattern = \
            AboutPreferences.Privacy.CONTENT_TRACKING_TRACKERS_ALWAYS_RADIO_NOT_SELECTED
        privacy_and_security_tab_pattern = AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED
        tracking_protection_shield_pattern = LocationBar.TRACKING_PROTECTION_SHIELD_ACTIVATED
        privacy_prefs_page_pattern = Pattern('about_preferences_privacy_address.png')
        cnn_site_logo_pattern = LocalWeb.CNN_LOGO

        # Access the about:preferences#privacy page
        navigate('about:preferences#privacy')
        privacy_prefs_page_displayed = exists(privacy_prefs_page_pattern, 20)
        assert_true(self, privacy_prefs_page_displayed, "The privacy preferences page is successfully displayed")

        # Enable the "Always" option from the Tracking Protection section
        always_block_trackers_not_selected_displayed = exists(always_block_trackers_not_selected_pattern, 3)
        if always_block_trackers_not_selected_displayed:
            click(always_block_trackers_not_selected_pattern)
        else:
            raise FindError('Can not find "Always" option from the Tracking Protection')

        privacy_and_security_tab_displayed = exists(privacy_and_security_tab_pattern, 3)
        if privacy_and_security_tab_displayed:
            click(privacy_and_security_tab_pattern)
        else:
            raise FindError('Can not find "Privacy and Security" tab')

        always_block_trackers_selected_displayed = \
            exists(AboutPreferences.Privacy.CONTENT_TRACKING_TRACKERS_ALWAYS_RADIO_SELECTED, 3)
        assert_true(self, always_block_trackers_selected_displayed,
                    '"Always" option from the Tracking Protection section is enabled')

        # Access the website
        new_tab()
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
        previous_tab()
        privacy_prefs_page_displayed = exists(privacy_prefs_page_pattern, 20)
        assert_true(self, privacy_prefs_page_displayed, "The privacy preferences page is successfully displayed")

        #  Click the "Exceptions" button from the Tracking protection section.
        click(AboutPreferences.Privacy.TRACKING_PROTECTION_EXCEPTIONS_BUTTON)
        track_protection_panel_displayed = exists(AboutPreferences.Privacy.Exceptions.EXCEPTIONS_CONTENT_BLOCKING_LABEL)
        assert_true(self, track_protection_panel_displayed, "The Tracking Protection panel is successfully displayed.")

        previously_accessed_site_displayed = exists(LocalWeb.CNN_CONTENT_BLOCKING_EXCEPTION)
        assert_true(self, previously_accessed_site_displayed,
                    "The previously accessed website is displayed as exception inside the panel.")

        # Click the "Remove Website" button and the "Save Changes"
        click(AboutPreferences.Privacy.Exceptions.REMOVE_WEBSITE_BUTTON)
        previously_accessed_site_displayed = exists(LocalWeb.CNN_CONTENT_BLOCKING_EXCEPTION)
        assert_false(self, previously_accessed_site_displayed, "The website is successfully removed from the panel.")

        click(AboutPreferences.Privacy.Exceptions.SAVE_CHANGES_BUTTON)

        # Access the removed website again.
        next_tab()
        website_displayed = exists(cnn_site_logo_pattern, 30)
        assert_true(self, website_displayed, 'The Website is successfully displayed')

        tracking_protection_shield_displayed = exists(tracking_protection_shield_pattern, 10)
        assert_true(self, tracking_protection_shield_displayed,
                    'The Tracking Protection shield is displayed near the address bar')
