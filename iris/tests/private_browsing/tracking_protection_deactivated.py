# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Tracking Protection can be successfully deactivated for both private and normal browsing sessions'
        self.test_case_id = '103330'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def click_on_action_item(self, action_item_before, action_item_after, action_item):
        """
        Method clicks on action item. Assume action_item is e.g. checkbox or radiobutton, which changes state after
        single click.

        :param action_item_before: Pattern of action item before click.
        :param action_item_after: Pattern of action item after click.
        :param action_item: Pattern or Region with item to click on.
            Note: Pattern or Region can contain only one action item
        :return: None
        """

        if action_item.__class__.__name__ is 'Pattern':
            try:
                option_with_action_item_location = find(action_item)
            except:
                raise FindError('Option {} is not available'.format(action_item))

            option_width, option_height = action_item.get_size()
            action_item_region = Region(option_with_action_item_location.x, option_with_action_item_location.y,
                                        option_width, option_height)

        elif action_item.__class__.__name__ is 'Region':
            action_item_region = action_item

        else:
            raise APIHelperError('Argument type is {}, only Pattern or Region allowed'
                                 .format(action_item.__class__.__name__))

        condition_before = exists(action_item_before, Settings.TINY_FIREFOX_TIMEOUT, action_item_region)
        condition_after = exists(action_item_after, Settings.TINY_FIREFOX_TIMEOUT, action_item_region)

        if condition_before:
            click(action_item_before, in_region=action_item_region)
            logger.debug('Action item clicked.')

        elif condition_after:
            logger.debug('Action item status changed successfully.')

        else:
            raise FindError('Action item was not found')


    def run(self):
        tracking_protection_shield_pattern = LocationBar.TRACKING_PROTECTION_SHIELD_ACTIVATED
        privacy_page_pattern = AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED
        cnn_logo_pattern = LocalWeb.CNN_LOGO
        custom_privacy_radio_pattern = Pattern('custom_privacy_radio.png')
        trackers_checked_pattern = Pattern('trackers_checked.png')
        trackers_unchecked_pattern = Pattern('trackers_unchecked.png')
        cookies_checked_pattern = Pattern('cookies_preference_checked.png')
        cookies_unchecked_pattern = Pattern('cookies_preference_unchecked.png')
        checkbox_checked_pattern = Pattern('checkbox_checked.png')
        checkbox_unchecked_pattern = Pattern('checkbox_unchecked.png')
        private_browsing_tab_pattern = Pattern('private_browsing_tab_logo.png')
        private_content_blocking_warning_pattern = Pattern('private_window_content_blocking_warning.png')
        info_button_pattern = Pattern('info_button.png')
        trackers_button_pattern = Pattern('trackers_button.png')
        trackers_popup_title_pattern = Pattern('trackers_popup_title.png')
        blocked_tracker_pattern = Pattern('blocked_tracker_label.png')
        trackers_icon_pattern = Pattern('trackers_icon.png')
        to_block_set_to_strict_pattern = Pattern('to_block_set_to_strict.png')

        new_tab()
        navigate('about:preferences#privacy')

        navigated_to_preferences = exists(privacy_page_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, navigated_to_preferences, 'The about:preferences#privacy page is successfully displayed.')

        custom_radio_found = exists(custom_privacy_radio_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, custom_radio_found, 'Custom" radio button from the "Content Blocking" section is displayed.')

        click(custom_privacy_radio_pattern, 1)

        custom_protection_popup_opened = exists(trackers_checked_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, custom_protection_popup_opened, 'The Custom panel is displayed.')

        click(trackers_checked_pattern)

        content_blocking_trackers_unchecked = exists(trackers_unchecked_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, content_blocking_trackers_unchecked, 'The trackers checkbox is unchecked successfully.')

        cookies_checked = exists(cookies_checked_pattern, Settings.FIREFOX_TIMEOUT)
        if cookies_checked:
            cookies_option_location = find(cookies_checked_pattern)
            cookies_width, cookies_height = cookies_checked_pattern.get_size()
            cookies_checkbox_region = Region(cookies_option_location.x - cookies_width,
                                             cookies_option_location.y - cookies_height,
                                             cookies_width * 2, cookies_height * 3)

            self.click_on_action_item(checkbox_checked_pattern, checkbox_unchecked_pattern, cookies_checkbox_region)

        content_blocking_cookies_unchecked = exists(cookies_unchecked_pattern)
        assert_true(self, content_blocking_cookies_unchecked, 'The cookies checkbox is unchecked successfully.')

        close_tab()

        new_tab()

        navigate('http://edition.cnn.com')

        cnn_logo_exists = exists(cnn_logo_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cnn_logo_exists, 'The website is successfully displayed.')

        tracking_protection_shield_common_window = exists(tracking_protection_shield_pattern,
                                                          Settings.SHORT_FIREFOX_TIMEOUT)
        assert_false(self, tracking_protection_shield_common_window,
                     'The Content blocking shield is not displayed near the address bar.')

        new_private_window()

        private_window_opened = exists(private_browsing_tab_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, private_window_opened, 'Private browsing window opened')

        content_blocking_private_displayed = exists(private_content_blocking_warning_pattern,
                                                    Settings.SHORT_FIREFOX_TIMEOUT)
        assert_false(self, content_blocking_private_displayed,
                     '"Some websites use trackers that can monitor your activity" etc. not displayed')

        navigate('http://edition.cnn.com')

        cnn_logo_exists = exists(cnn_logo_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cnn_logo_exists, 'The website is successfully displayed.')

        tracking_protection_shield_private_window = exists(tracking_protection_shield_pattern,
                                                           Settings.SHORT_FIREFOX_TIMEOUT)
        assert_false(self, tracking_protection_shield_private_window,
                     'The Content blocking shield is not displayed near the address bar')

        info_button_located = exists(info_button_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, info_button_located, 'The "i button" (Info button) is located near the address bar')

        click(info_button_pattern)

        open_trackers_list_button_located = exists(trackers_button_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, open_trackers_list_button_located, 'The site information panel is displayed.')

        click(trackers_button_pattern)

        trackers_popup_displayed = exists(trackers_popup_title_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, trackers_popup_displayed, 'Trackers popup window is displayed on screen')

        list_of_active_trackers_displayed = exists(trackers_icon_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, list_of_active_trackers_displayed, 'A list of active trackers is successfully displayed.')

        trackers_blocked = exists(blocked_tracker_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_false(self, trackers_blocked, 'The trackers are not blocked.')

        to_block_set_to_strict_located = exists(to_block_set_to_strict_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, to_block_set_to_strict_located,
                    '\'To block all trackers, set content blocking to "Strict"\' is displayed')

        close_window()



