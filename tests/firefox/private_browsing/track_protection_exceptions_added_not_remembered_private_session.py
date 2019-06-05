# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Tracking protection exceptions can be added'
                    ' but can\'t be remembered using private browsing session',
        test_case_id='107718',
        test_suite_id='1826',
        locale=['en-US'],
    )
    def run(self, firefox):
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
        private_window_opened = exists(PrivateWindow.private_window_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert private_window_opened is True, 'Private window opened.'

        navigate('https://itisatrap.org/firefox/its-a-tracker.html')
        tracked_site_loaded = exists(firefox_tracker_site_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert tracked_site_loaded is True, 'The website is successfully displayed.'

        tracking_protection_shield_displayed = exists(LocationBar.TRACKING_PROTECTION_SHIELD_ACTIVATED)
        assert tracking_protection_shield_displayed is True, 'The tracking protection shield is displayed.'

        third_party_trackers_blocked = exists(third_party_tracker_correctly_blocked_pattern)
        assert third_party_trackers_blocked is True, 'A "simulated third-party tracker was correctly blocked" ' \
                                                     'phrase is displayed.'

        first_party_tracker_correctly_loaded = exists(first_party_tracker_correctly_blocked_text_pattern)
        assert first_party_tracker_correctly_loaded is True, 'A "simulated first-party tracker was correctly loaded"' \
                                                             ' phrase is displayed.'

        dnt_sent_correctly = exists(dnt_signal_correctly_sent_pattern)
        assert dnt_sent_correctly is True, 'The "DNT signal was correctly send" phrase is displayed.'

        click(LocationBar.TRACKING_PROTECTION_SHIELD_ACTIVATED)

        protection_popup_opened = exists(blocking_turn_off_pattern)
        assert protection_popup_opened is True, "The site information panel is displayed."

        click(blocking_turn_off_pattern)

        tracking_protection_shield_deactivated_exists = exists(LocationBar.TRACKING_PROTECTION_SHIELD_DEACTIVATED)
        assert tracking_protection_shield_deactivated_exists is True, 'The tracking protection shield is displayed' \
                                                                      ' as deactivated (strikethrough).'

        page_loaded = exists(firefox_tracker_site_logo_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert page_loaded is True, 'The website successfully refreshes.'

        restore_firefox_focus()
        hover(LocationBar.TRACKING_PROTECTION_SHIELD_DEACTIVATED)

        tracking_message_appeared = exists(LocationBar.TRACKING_CONTENT_DETECTED_MESSAGE)
        assert tracking_message_appeared is True, 'A "Tracking content detected" tooltip message displayed.'

        incorrectly_loaded_third_party_tracker = exists(incorrectly_loaded_third_party_tracker_pattern)
        assert incorrectly_loaded_third_party_tracker is True, 'A "simulated third-party tracker' \
                                                               ' was incorrectly loaded" phrase is displayed.'

        first_party_tracker_correctly_loaded_again = exists(first_party_tracker_correctly_blocked_text_pattern)
        assert first_party_tracker_correctly_loaded_again is True, 'A "simulated first-party tracker was ' \
                                                                   'correctly loaded" phrase is displayed again.'

        dnt_sent_correctly_again = exists(dnt_signal_correctly_sent_pattern)
        assert dnt_sent_correctly_again is True, 'The "DNT signal was correctly send" phrase is displayed again.'

        restore_firefox_focus()
        click(LocationBar.TRACKING_PROTECTION_SHIELD_DEACTIVATED)

        tracking_protection_popup_opened = exists(open_trackers_list_pattern)
        assert tracking_protection_popup_opened is True, 'Tracking protection popup opened.'

        click(open_trackers_list_pattern)

        trackers_list_opened = exists(tracker_site_in_list_pattern)
        assert trackers_list_opened is True, 'A list of unblocked trackers is successfully displayed.'

        navigate('about:preferences#privacy')
        preferences_opened = exists(manage_exceptions_button_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert preferences_opened is True, 'The about:preferences#privacy page is successfully displayed.'

        click(manage_exceptions_button_pattern)

        exceptions_list_empty = exists(empty_exc_list_pattern.similar(0.6))
        assert exceptions_list_empty is True, 'The previously accessed website is not displayed' \
                                              ' inside the Tracking Protection exceptions panel.'

        close_window()
