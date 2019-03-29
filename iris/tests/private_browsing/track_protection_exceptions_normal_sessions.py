# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Tracking protection exceptions can be successfully added, ' \
                    'remembered and removed from normal browsing session'
        self.test_case_id = '107717'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def run(self):
        remove_website_button_pattern = AboutPreferences.Privacy.Exceptions.REMOVE_WEBSITE_BUTTON
        privacy_page_pattern = AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED
        tracking_protection_shield_pattern = LocationBar.TRACKING_PROTECTION_SHIELD_ACTIVATED
        tracking_protection_shield_deactivated_pattern = LocationBar.TRACKING_PROTECTION_SHIELD_DEACTIVATED
        tracking_content_detected_pattern = LocationBar.TRACKING_CONTENT_DETECTED_MESSAGE

        exceptions_content_blocking_panel_pattern = \
                AboutPreferences.Privacy.Exceptions.EXCEPTIONS_CONTENT_BLOCKING_LABEL

        turn_off_blocking_pattern = Pattern('turn_off_blocking_for_this_site.png')
        manage_exceptions_button_pattern = Pattern('manage_exceptions_button.png')
        privacy_strict_checkbox_unchecked_pattern = Pattern('privacy_strict_checkbox_unchecked.png')
        privacy_strict_checkbox_checked_pattern = Pattern('privacy_strict_checkbox_checked.png')
        firefox_tracker_site_content_pattern = Pattern('firefox_tracker_site_content.png')
        third_party_tracker_correctly_blocked_text = Pattern('simulated_third_party_tracker_correctly_blocked_text.png')
        first_party_tracker_correctly_blocked_text = Pattern('simulated_first_party_tracker_correctly_blocked_text.png')
        dnt_signal_correctly_sent_text = Pattern('dnt_signal_correctly_sent_text.png')
        third_party_tracker_incorrectly_loaded_text = \
            Pattern('simulated_third_party_tracker_incorrectly_loaded_text.png')
        itstrap_site_exception_selected_pattern = Pattern('itstrap_site_exception_selected.png')

        navigate('about:preferences#privacy')
        navigated_to_preferences = exists(privacy_page_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, navigated_to_preferences, 'The about:preferences#privacy page is successfully displayed.')

        privacy_strict_checkbox_unchecked_displayed = exists(privacy_strict_checkbox_unchecked_pattern)
        if privacy_strict_checkbox_unchecked_displayed:
            click(privacy_strict_checkbox_unchecked_pattern)
        else:
            raise FindError('The "Strict" content blocking option was not found')

        click(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED)

        privacy_strict_checkbox_checked_displayed = exists(privacy_strict_checkbox_checked_pattern)
        assert_true(self, privacy_strict_checkbox_checked_displayed,
                    'The "Strict" content blocking option was successfully saved')

        navigate('https://itisatrap.org/firefox/its-a-tracker.html')
        firefox_tracker_site_logo_displayed = exists(firefox_tracker_site_content_pattern)
        assert_true(self, firefox_tracker_site_logo_displayed, 'The website is successfully displayed.')

        tracking_protection_shield_displayed = exists(tracking_protection_shield_pattern)
        assert_true(self, tracking_protection_shield_displayed,
                    'The Tracking protection shield is displayed near the address bar.')

        third_party_tracker_correctly_blocked_displayed = exists(third_party_tracker_correctly_blocked_text)
        assert_true(self, third_party_tracker_correctly_blocked_displayed,
                    'Simulated third-party tracker was correctly blocked is displayed.')

        first_party_tracker_correctly_blocked_displayed = exists(first_party_tracker_correctly_blocked_text)
        assert_true(self, first_party_tracker_correctly_blocked_displayed,
                    'Simulated first-party tracker was correctly loaded is displayed.')

        dnt_signal_correctly_sent_displayed = exists(dnt_signal_correctly_sent_text)
        assert_true(self, dnt_signal_correctly_sent_displayed, 'The DNT signal was correctly sent is displayed.')

        click(tracking_protection_shield_pattern)
        click(turn_off_blocking_pattern)

        firefox_tracker_site_logo_displayed = exists(firefox_tracker_site_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_tracker_site_logo_displayed, 'Site is reloaded after turning off content blocking')

        tracking_protection_shield_deactivated_displayed = exists(tracking_protection_shield_deactivated_pattern)
        assert_true(self, tracking_protection_shield_deactivated_displayed,
                    'The tracking protection shield is displayed as deactivated (strikethrough).')

        mouse_move(tracking_protection_shield_deactivated_pattern)
        tracking_content_detected_pattern_displayed = exists(tracking_content_detected_pattern, DEFAULT_SYSTEM_DELAY)
        assert_true(self, tracking_content_detected_pattern_displayed,
                    'On hover, the tracking protection shield displays a "Tracking content detected" tooltip message.')

        third_party_tracker_incorrectly_loaded_displayed = exists(third_party_tracker_incorrectly_loaded_text)
        assert_true(self, third_party_tracker_incorrectly_loaded_displayed,
                    'Simulated third-party tracker was incorrectly loaded is displayed.')

        first_party_tracker_correctly_blocked_displayed = exists(first_party_tracker_correctly_blocked_text)
        assert_true(self, first_party_tracker_correctly_blocked_displayed,
                    'Simulated first-party tracker was correctly loaded is displayed.')

        dnt_signal_correctly_sent_displayed = exists(dnt_signal_correctly_sent_text)
        assert_true(self, dnt_signal_correctly_sent_displayed, 'The DNT signal was correctly sent is displayed.')

        navigate('about:preferences#privacy')

        click(manage_exceptions_button_pattern)
        exceptions_content_blocking_panel_displayed = exists(exceptions_content_blocking_panel_pattern)
        assert_true(self, exceptions_content_blocking_panel_displayed,
                    'The Exceptions - Content Blocking panel is successfully displayed.')

        itstrap_site_exception_displayed = exists(itstrap_site_exception_selected_pattern)
        assert_true(self, itstrap_site_exception_displayed,
                    'The previously accessed website is displayed as exception inside the panel.')

        click(remove_website_button_pattern)
        click(AboutPreferences.Privacy.Exceptions.SAVE_CHANGES_BUTTON)
        click(manage_exceptions_button_pattern)

        itstrap_site_exception_displayed = exists(itstrap_site_exception_selected_pattern)
        assert_false(self, itstrap_site_exception_displayed, 'The website is successfully removed from the panel.')

        navigate('https://itisatrap.org/firefox/its-a-tracker.html')
        firefox_tracker_site_logo_displayed = exists(firefox_tracker_site_content_pattern)
        assert_true(self, firefox_tracker_site_logo_displayed, 'The website is successfully displayed.')

        tracking_protection_shield_displayed = exists(tracking_protection_shield_pattern)
        assert_true(self, tracking_protection_shield_displayed,
                    'The Tracking protection shield is displayed near the address bar.')

        third_party_tracker_correctly_blocked_displayed = exists(third_party_tracker_correctly_blocked_text)
        assert_true(self, third_party_tracker_correctly_blocked_displayed,
                    'Simulated third-party tracker was correctly blocked is displayed.')

        first_party_tracker_correctly_blocked_displayed = exists(first_party_tracker_correctly_blocked_text)
        assert_true(self, first_party_tracker_correctly_blocked_displayed,
                    'Simulated first-party tracker was correctly loaded is displayed.')

        dnt_signal_correctly_sent_displayed = exists(dnt_signal_correctly_sent_text)
        assert_true(self, dnt_signal_correctly_sent_displayed, 'The DNT signal was correctly sent is displayed.')
