# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Tracking protection can be deactivated from the about:privatebrowsing page'
        self.test_case_id = '107432'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def run(self):
        # Open a new private browsing session
        new_private_window()

        private_window_displayed = exists(PrivateWindow.private_window_pattern)
        assert_true(self, private_window_displayed, "The private browsing window is displayed")

        # Click on the Tracking Protections switch
        tracking_protection_switch_on_displayed = exists(PrivateWindow.TRACKING_PROTECTION_SWITCH_ON, 5)
        if tracking_protection_switch_on_displayed:
            click(PrivateWindow.TRACKING_PROTECTION_SWITCH_ON)
        else:
            raise FindError('Can not find the Tracking Protection switch (turned ON)')

        tracking_protection_switch_off_displayed = exists(PrivateWindow.TRACKING_PROTECTION_SWITCH_OFF, 5)
        assert_true(self, tracking_protection_switch_off_displayed,
                    'The Tracking Protection switch is turned off')

        tracking_protection_shield_disabled_displayed = exists(PrivateWindow.TRACKING_PROTECTION_SHIELD_DEACTIVATED, 5)
        assert_true(self, tracking_protection_shield_disabled_displayed,
                    'The Tracking Protection shield is displayed as disabled')

        # Access the website
        new_tab()
        navigate('https://edition.cnn.com')

        website_displayed = exists(LocalWeb.CNN_LOGO, 30)
        assert_true(self, website_displayed, 'The Website is successfully displayed')

        tracking_protection_shield_activated_displayed = exists(LocationBar.TRACKING_PROTECTION_SHIELD_ACTIVATED, 10)
        assert_false(self, tracking_protection_shield_activated_displayed,
                     'The Tracking Protection shield (activated) is not displayed near the address bar')

        tracking_protection_shield_deactivated_displayed = exists(LocationBar.TRACKING_PROTECTION_SHIELD_DEACTIVATED, 10)
        assert_false(self, tracking_protection_shield_deactivated_displayed,
                     'The Tracking Protection shield (deactivated) is not displayed near the address bar')
