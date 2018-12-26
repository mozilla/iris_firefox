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
        do_not_track_label_pattern = Pattern('do_not_track_label.png')
        always_block_tracker_not_selected_pattern = \
            AboutPreferences.Privacy.CONTENT_TRACKING_TRACKERS_ALWAYS_RADIO_NOT_SELECTED
        privacy_page_pattern = AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED
        always_block_tracker_selected_pattern = AboutPreferences.Privacy.CONTENT_TRACKING_TRACKERS_ALWAYS_RADIO_SELECTED
        cnn_logo_pattern = LocalWeb.CNN_LOGO
        tracking_protection_shield_pattern = LocationBar.TRACKING_PROTECTION_SHIELD_ACTIVATED
        tracking_protection_shield_deactivated_pattern = LocationBar.TRACKING_PROTECTION_SHIELD_DEACTIVATED
        tracking_content_detected_pattern = LocationBar.TRACKING_CONTENT_DETECTED_MESSAGE
        turn_off_blocking_pattern = Pattern('turn_off_blocking_for_this_site.png')
        manage_exceptions_button_pattern = Pattern('manage_exceptions_button.png')
        tracking_protection_panel_pattern = Pattern('tracking_protection_panel_label.png')
        site_displayed_as_exception_pattern = Pattern('site_displayed_as_exception.png')
        remove_website_button_pattern = Pattern('remove_website_button.png')
        save_changes_button_pattern = Pattern('save_changes_button.png')

        navigate('about:preferences#privacy')
        navigated_to_preferences = exists(privacy_page_pattern, 10)
        assert_true(self, navigated_to_preferences, 'The about:preferences#privacy page is successfully displayed.')
        do_not_track_label_exists = exists(do_not_track_label_pattern, 10)

        try:
            click(always_block_tracker_not_selected_pattern, DEFAULT_FX_DELAY)
            type(Key.TAB)
            wait(always_block_tracker_selected_pattern, 10)
        except FindError:
            raise FindError('Always block is not selected')
        always_block_tracker_selected_exists = exists(always_block_tracker_selected_pattern, 10)

        if do_not_track_label_exists and always_block_tracker_selected_exists:
            assert_true(self, always_block_tracker_selected_exists, 'The option is successfully saved.')

        navigate('http://edition.cnn.com/')
        cnn_logo_exists = exists(cnn_logo_pattern, 80)
        tracking_protection_shield_exists = exists(tracking_protection_shield_pattern, 20)

        assert_true(self, cnn_logo_exists,
                    'The website is successfully displayed.')
        assert_true(self, tracking_protection_shield_exists,
                    'The Tracking protection shield is displayed near the address bar.')

        shield_location = find(tracking_protection_shield_pattern)

        click(shield_location, DEFAULT_FX_DELAY)
        turn_off_blocking_exists = exists(turn_off_blocking_pattern, 40)
        if turn_off_blocking_exists:
            click(turn_off_blocking_pattern, DEFAULT_FX_DELAY)

        tracking_protection_shield_deactivated_exists = exists(tracking_protection_shield_deactivated_pattern, 40)
        assert_true(self, tracking_protection_shield_deactivated_exists,
                    'The tracking protection shield is displayed as deactivated (red strikethrough).')

        hover(tracking_protection_shield_deactivated_pattern, 40)
        tracking_content_detected_exists = exists(tracking_content_detected_pattern, 40)
        assert_true(self, tracking_content_detected_exists,
                    'On hover, the tracking protection shield displays a "Tracking content detected" tooltip message. '
                    'Websites content that contain tracking elements is displayed on the page.')

        navigate('about:preferences#privacy')
        navigated_to_preferences = exists(privacy_page_pattern, 40)
        assert_true(self, navigated_to_preferences,
                    'The about:preferences#privacy page is successfully displayed.')

        click(manage_exceptions_button_pattern, DEFAULT_FX_DELAY)
        tracking_protection_panel_exists = exists(tracking_protection_panel_pattern, 40)
        assert_true(self, tracking_protection_panel_exists,
                    'The Tracking Protection panel is successfully displayed.')

        site_displayed_as_exception_exists = exists(site_displayed_as_exception_pattern, 40)
        assert_true(self, site_displayed_as_exception_exists,
                    'The previously accessed website is displayed as exception inside the panel.')

        try:
            click(remove_website_button_pattern, DEFAULT_FX_DELAY)
            site_displayed_as_exception_not_exists = wait_vanish(site_displayed_as_exception_pattern, 40)
            click(save_changes_button_pattern, DEFAULT_FX_DELAY)
            assert_true(self, site_displayed_as_exception_not_exists,
                        'The website is successfully removed from the panel.')
        except FindError:
            raise FindError('Previous site still exists')

        navigate('http://edition.cnn.com/')
        cnn_logo_exists = exists(cnn_logo_pattern, 80)
        tracking_protection_shield_exists = exists(tracking_protection_shield_pattern, 20)

        assert_true(self, cnn_logo_exists, 'The website is successfully displayed.')

        assert_true(self, tracking_protection_shield_exists,
                    'The Tracking protection shield is displayed near the address bar.')