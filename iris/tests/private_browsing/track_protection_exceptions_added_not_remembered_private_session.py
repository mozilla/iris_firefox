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
        blocking_turn_off_pattern = Pattern('turn_off_blocking_for_site_button.png')
        empty_exc_list_pattern = Pattern('empty_exc_list.png')
        manage_exceptions_button_pattern = Pattern('manage_exceptions_button.png')
        firefox_tracker_site_logo_pattern = Pattern('firefox_tracker_site_logo.png')
        third_party_tracker_correctly_blocked_pattern = \
            Pattern('simulated_third_party_tracker_correctly_blocked_text.png')
        incorrectly_loaded_third_party_tracker_pattern = \
            Pattern('simulated_third_party_tracker_incorrectly_loaded_text.png')
        first_party_tracker_correctly_blocked_text_pattern = \
            Pattern('simulated_first_party_tracker_correctly_blocked_text.png')
        dnt_signal_correctly_sent_pattern = Pattern('dnt_signal_correctly_sent_text.png')
        open_trackers_list_pattern = Pattern('open_trackers_list.png')
        tracker_site_in_list_pattern = Pattern('tracker_testsite_in_list.png')

        new_private_window()
        private_window_opened = exists(PrivateWindow.private_window_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, private_window_opened, 'Private window opened.')

        navigate('https://itisatrap.org/firefox/its-a-tracker.html')
        tracked_site_loaded = exists(firefox_tracker_site_logo_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, tracked_site_loaded, 'The website is successfully displayed.')

        tracking_protection_shield_displayed = exists(LocationBar.TRACKING_PROTECTION_SHIELD_ACTIVATED)
        assert_true(self, tracking_protection_shield_displayed, 'The tracking protection shield is displayed.')

        third_party_trackers_blocked = exists(third_party_tracker_correctly_blocked_pattern)
        assert_true(self, third_party_trackers_blocked,
                    'A "simulated third-party tracker was correctly blocked" phrase is displayed.')

        first_party_tracker_correctly_loaded = exists(first_party_tracker_correctly_blocked_text_pattern)
        assert_true(self, first_party_tracker_correctly_loaded,
                    'A "simulated first-party tracker was correctly loaded" phrase is displayed.')

        dnt_sent_correctly = exists(dnt_signal_correctly_sent_pattern)
        assert_true(self, dnt_sent_correctly, 'The "DNT signal was correctly send" phrase is displayed.')

        click(LocationBar.TRACKING_PROTECTION_SHIELD_ACTIVATED)

        protection_popup_opened = exists(blocking_turn_off_pattern)
        assert_true(self, protection_popup_opened, "The site information panel is displayed.")

        click(blocking_turn_off_pattern)

        tracking_protection_shield_deactivated_exists = exists(LocationBar.TRACKING_PROTECTION_SHIELD_DEACTIVATED)
        assert_true(self, tracking_protection_shield_deactivated_exists,
                    'The tracking protection shield is displayed as deactivated (strikethrough).')

        page_loaded = exists(firefox_tracker_site_logo_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, page_loaded, 'The website successfully refreshes.')

        restore_firefox_focus()
        hover(LocationBar.TRACKING_PROTECTION_SHIELD_DEACTIVATED)

        tracking_message_appeared = exists(LocationBar.TRACKING_CONTENT_DETECTED_MESSAGE)
        assert_true(self, tracking_message_appeared, 'A "Tracking content detected" tooltip message displayed.')

        incorrectly_loaded_third_party_tracker = exists(incorrectly_loaded_third_party_tracker_pattern)
        assert_true(self, incorrectly_loaded_third_party_tracker,
                    'A "simulated third-party tracker was incorrectly loaded" phrase is displayed.')

        first_party_tracker_correctly_loaded_again = exists(first_party_tracker_correctly_blocked_text_pattern)
        assert_true(self, first_party_tracker_correctly_loaded_again,
                    'A "simulated first-party tracker was correctly loaded" phrase is displayed again.')

        dnt_sent_correctly_again = exists(dnt_signal_correctly_sent_pattern)
        assert_true(self, dnt_sent_correctly_again, 'The "DNT signal was correctly send" phrase is displayed again.')

        restore_firefox_focus()
        click(LocationBar.TRACKING_PROTECTION_SHIELD_DEACTIVATED)

        tracking_protection_popup_opened = exists(open_trackers_list_pattern)
        assert_true(self, tracking_protection_popup_opened, 'Tracking protection popup opened.')

        click(open_trackers_list_pattern)

        trackers_list_opened = exists(tracker_site_in_list_pattern)
        assert_true(self, trackers_list_opened, 'A list of unblocked trackers is successfully displayed.')

        navigate('about:preferences#privacy')
        preferences_opened = exists(manage_exceptions_button_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, preferences_opened, 'The about:preferences#privacy page is successfully displayed.')

        click(manage_exceptions_button_pattern)

        exceptions_list_empty = exists(empty_exc_list_pattern.similar(0.6))
        assert_true(self, exceptions_list_empty,
                    'The previously accessed website is not displayed inside the Tracking Protection exceptions panel.')

        close_window()
