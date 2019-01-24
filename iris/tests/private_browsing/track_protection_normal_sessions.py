# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Tracking Protection can be activated on Normal sessions as well ' \
                    '[The Tracking Protection Shield does not appear on step 4]'
        self.test_case_id = '103329'
        self.test_suite_id = '1826'
        self.locales = ['en-US']
        self.exclude = Platform.ALL

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        return

    def run(self):
        do_not_track_always_selected_pattern = Pattern('do_not_track_option_always_selected_radio.png')
        do_not_track_always_unselected_pattern = Pattern('do_not_track_option_always_unselected_radio.png')

        privacy_and_security_tab_pattern = AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED
        tracking_protection_shield_pattern = LocationBar.TRACKING_PROTECTION_SHIELD_ACTIVATED
        privacy_prefs_page_pattern = Pattern('about_preferences_privacy_address.png')
        cnn_site_logo_pattern = Pattern('cnn_logo.png')

        # Access the about:preferences#privacy page
        navigate('about:preferences#privacy')
        privacy_prefs_page_displayed = exists(privacy_prefs_page_pattern, 20)
        assert_true(self, privacy_prefs_page_displayed, "The privacy preferences page is successfully displayed")

        # Enable the "Always" option from the Tracking Protection section
        do_not_track_always_selected_displayed = exists(do_not_track_always_selected_pattern, 3)
        if do_not_track_always_selected_displayed:
            click(do_not_track_always_unselected_pattern)
        else:
            raise FindError('Can not find "Always" option from the Send websites a Do Not Track signal')

        if not Settings.is_mac():
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

        website_displayed = exists(cnn_site_logo_pattern, 60)
        assert_true(self, website_displayed, 'The Website is successfully displayed')

        tracking_protection_shield_displayed = exists(tracking_protection_shield_pattern, 10)
        assert_true(self, tracking_protection_shield_displayed,
                    'The Tracking Protection shield is displayed near the address bar')
