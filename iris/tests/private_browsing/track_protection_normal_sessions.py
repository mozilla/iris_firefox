# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Tracking Protection can be activated on Normal sessions as well'
        self.test_case_id = '103329'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def run(self):
        preferences_privacy_find_field_pattern = Pattern('preferences_privacy_find_field.png')
        send_track_data_pattern = Pattern('send_websites_do_not_track_data_option.png')
        do_not_track_unselected_pattern = Pattern('do_not_track_option_always_unselected_radio.png')
        do_not_track_selected_pattern = Pattern('do_not_track_option_always_selected_radio.png')
        tracker_website_content_pattern = Pattern('tracker_website_content.png')
        do_not_track_signal_displayed_pattern = Pattern('do_not_track_signal_displayed.png')

        navigate('about:preferences#privacy')

        privacy_preferences_page_displayed = exists(preferences_privacy_find_field_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, privacy_preferences_page_displayed, 'The privacy preferences page is successfully displayed')

        click(preferences_privacy_find_field_pattern)

        paste('Send websites a')

        send_track_data_found = scroll_until_pattern_found(send_track_data_pattern, scroll, (-25,), 20, 1)
        assert_true(self, send_track_data_found, 'Send websites option found')

        send_track_data_pattern_width, send_track_data_pattern_height = send_track_data_pattern.get_size()

        send_websites_option_position = find(send_track_data_pattern)
        send_websites_option_region = Region(send_websites_option_position.x-100, send_websites_option_position.y,
                                             send_track_data_pattern_width+100, send_track_data_pattern_height+100)

        send_websites_option_unchecked = exists(do_not_track_unselected_pattern, Settings.FIREFOX_TIMEOUT,
                                                send_websites_option_region)
        assert_true(self, send_websites_option_unchecked, 'Do not track "Always" option is displayed unchecked')

        click(do_not_track_unselected_pattern, in_region=send_websites_option_region)

        do_not_track_selected = exists(do_not_track_selected_pattern, Settings.FIREFOX_TIMEOUT,
                                       send_websites_option_region)
        assert_true(self, do_not_track_selected, 'Do not track "Always" option checked')

        new_tab()
        navigate('https://itisatrap.org/firefox/its-a-tracker.html')

        website_loaded = exists(tracker_website_content_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, website_loaded, 'The Website is successfully loaded')

        do_not_track_signal_displayed = exists(do_not_track_signal_displayed_pattern)
        assert_true(self, do_not_track_signal_displayed, 'The DNT (Do not track) signal is displayed as correctly sent')
