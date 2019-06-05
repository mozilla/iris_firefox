# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Tracking Protection can be activated on Normal sessions as well',
        test_case_id='103329',
        test_suite_id='1826',
        locale=['en-US'],
    )
    def run(self, firefox):
        preferences_privacy_find_field_pattern = Pattern('preferences_privacy_find_field.png')
        send_track_data_pattern = Pattern('send_websites_do_not_track_data_option.png')
        do_not_track_unselected_pattern = Pattern('do_not_track_option_always_unselected_radio.png')
        do_not_track_selected_pattern = Pattern('do_not_track_option_always_selected_radio.png')
        tracker_website_content_pattern = Pattern('tracker_website_content.png')
        do_not_track_signal_displayed_pattern = Pattern('do_not_track_signal_displayed.png')

        navigate('about:preferences#privacy')

        privacy_preferences_page_displayed = exists(preferences_privacy_find_field_pattern,
                                                    FirefoxSettings.FIREFOX_TIMEOUT)
        assert privacy_preferences_page_displayed is True, 'The privacy preferences page is successfully displayed'

        click(preferences_privacy_find_field_pattern)

        paste('Send websites a')

        send_track_data_found = scroll_until_pattern_found(send_track_data_pattern, scroll_down, (25,), 20, 1)
        assert send_track_data_found is True, 'Send websites option found'

        send_track_data_pattern_width, send_track_data_pattern_height = send_track_data_pattern.get_size()

        send_websites_option_position = find(send_track_data_pattern)
        send_websites_option_region = Region(send_websites_option_position.x-100, send_websites_option_position.y,
                                             send_track_data_pattern_width+100, send_track_data_pattern_height+100)

        send_websites_option_unchecked = exists(do_not_track_unselected_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                                send_websites_option_region)
        assert send_websites_option_unchecked is True, 'Do not track "Always" option is displayed unchecked'

        click(do_not_track_unselected_pattern, region=send_websites_option_region)

        do_not_track_selected = exists(do_not_track_selected_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                       send_websites_option_region)
        assert do_not_track_selected is True, 'Do not track "Always" option checked'

        new_tab()
        navigate('https://itisatrap.org/firefox/its-a-tracker.html')

        website_loaded = exists(tracker_website_content_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert website_loaded is True, 'The Website is successfully loaded'

        do_not_track_signal_displayed = exists(do_not_track_signal_displayed_pattern)
        assert do_not_track_signal_displayed is True, 'The DNT (Do not track) signal is displayed as correctly sent'
