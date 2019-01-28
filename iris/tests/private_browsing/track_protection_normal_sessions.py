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
        # self.exclude = Platform.ALL

    def run(self):
        do_not_track_unselected_pattern = Pattern('do_not_track_option_always_unselected_radio.png')
        do_not_track_selected_pattern = Pattern('do_not_track_option_always_selected_radio.png')
        preferences_privacy_find_field_pattern = Pattern('preferences_privacy_find_field.png')
        tracker_website_content_pattern = Pattern('tracker_website_content.png')
        send_websites_do_not_track_data_pattern = Pattern('send_websites_do_not_track_data_option.png')
        do_not_track_signal_displayed_pattern = Pattern('do_not_track_signal_displayed.png')

        navigate('about:preferences#privacy')
        privacy_preferences_page_displayed = exists(preferences_privacy_find_field_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, privacy_preferences_page_displayed, 'The privacy preferences page is successfully displayed')

        click(preferences_privacy_find_field_pattern)
        paste('Send websites a')

        send_websites_do_not_track_data_found = exists(send_websites_do_not_track_data_pattern)
        assert_true(self, send_websites_do_not_track_data_found, 'Send websites option found')

        send_websites_option_position = find(send_websites_do_not_track_data_pattern)
        send_websites_option_region = Region(send_websites_option_position.x-100, send_websites_option_position.y,
                                             width=SCREEN_WIDTH, height=SCREEN_HEIGHT - send_websites_option_position.y)

        send_websites_option_unchecked = exists(do_not_track_unselected_pattern, DEFAULT_FIREFOX_TIMEOUT,
                                             in_region=send_websites_option_region)
        assert_true(self, send_websites_option_unchecked, 'Do not track "Always" option unchecked')
        click(do_not_track_unselected_pattern, in_region=send_websites_option_region)

        do_not_track_selected = exists(do_not_track_selected_pattern, DEFAULT_FIREFOX_TIMEOUT,
                                       in_region=send_websites_option_region)
        assert_true(self, do_not_track_selected, 'Do not track "Always" option checked')

        new_tab()
        navigate('https://itisatrap.org/firefox/its-a-tracker.html')

        website_loaded = exists(tracker_website_content_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, website_loaded, 'The Website is successfully loaded')

        do_not_track_signal_displayed = exists(do_not_track_signal_displayed_pattern)
        assert_true(self, do_not_track_signal_displayed,
                    'The DNT (Do not track) signal is displayed as correctly sent.')
