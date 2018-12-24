from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Tracking Protection can be successfully deactivated for both private and normal browsing sessions'
        self.test_case_id = '103330'
        self.test_suite_id = '1579'
        self.locales = ['en-US']

    def run(self):
        custom_privacy_radio_pattern = Pattern('custom_privacy_radio.png')
        trackers_checked_pattern = Pattern('trackers_checked.png')
        trackers_unchecked_pattern = Pattern('trackers_unchecked.png')
        tracking_protection_shield = LocationBar.TRACKING_PROTECTION_SHIELD_ACTIVATED
        private_browsing_tab_pattern = Pattern('private_browsing_tab_logo.png')
        private_content_blocking_warning_pattern = Pattern('private_window_content_blocking_warning.png')
        info_button_pattern = Pattern('info_button.png')
        open_trackers_list_pattern = Pattern('trackers_button.png')
        trackers_list_header_pattern = Pattern('trackers_list_header.png')

        new_tab()
        select_location_bar()
        navigate('about:preferences#privacy')
        custom_radio_found = exists(custom_privacy_radio_pattern)
        assert_true(self, custom_radio_found, 'custom_radio_found')
        custom_radiobutton = find(custom_privacy_radio_pattern)
        click(custom_radiobutton)

        custom_protection_popup_opened = exists(trackers_checked_pattern)
        assert_true(self,
                    custom_protection_popup_opened,
                    'Custom content blocking menu unfolded')

        click(trackers_unchecked_pattern)
        hover(Location(SCREEN_WIDTH, SCREEN_HEIGHT / 2), duration=0.5)
        content_blocking_trackers_unchecked = exists(trackers_unchecked_pattern)
        assert_true(self,
                    content_blocking_trackers_unchecked,
                    'Trackers unchecked')

        close_tab()
        new_tab()
        navigate('http://edition.cnn.com')
        tracking_protection_shield_common_window = exists(tracking_protection_shield,
                                                          timeout=10)
        assert_true(self, tracking_protection_shield_common_window,
                    'Tracking protection shield found in common window')

        new_private_window()
        private_window_opened = exists(private_browsing_tab_pattern)
        assert_true(self, private_window_opened,
                    'Private browsing window opened')

        content_blocking_private_not_displayed = not exists(private_content_blocking_warning_pattern)
        assert_true(self, content_blocking_private_not_displayed,
                    '\'Some websites use trackers that can monitor your activity\' etc. not displayed')
        navigate('http://edition.cnn.com')
        tracking_protection_shield_private_window = exists(tracking_protection_shield,
                                                           timeout=10)
        info_button_located = exists(info_button_pattern)
        assert_true(self, tracking_protection_shield_private_window and info_button_located,
                    'Tracking protection shield found in private window')

        info_button = find(info_button_pattern)
        click(info_button)
        open_trackers_list_button_located = exists(open_trackers_list_pattern)
        assert_true(self, open_trackers_list_button_located,
                    'Info popup opened')

        open_trackers_list_button = find(open_trackers_list_pattern)
        click(open_trackers_list_button)
        hover(Location(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        trackers_list_header_located = exists(trackers_list_header_pattern)
        assert_true(self,
                    trackers_list_header_located,
                    'Trackers list opened')
        close_window()
