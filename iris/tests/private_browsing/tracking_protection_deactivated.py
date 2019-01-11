from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Tracking Protection can be successfully deactivated for both private and normal browsing sessions'
        self.test_case_id = '103330'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def run(self):
        tracking_protection_shield_pattern = LocationBar.TRACKING_PROTECTION_SHIELD_ACTIVATED
        privacy_page_pattern = AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED
        cnn_logo_pattern = LocalWeb.CNN_LOGO

        custom_privacy_radio_pattern = Pattern('custom_privacy_radio.png')
        trackers_checked_pattern = Pattern('trackers_checked.png')
        trackers_unchecked_pattern = Pattern('trackers_unchecked.png')
        private_browsing_tab_pattern = Pattern('private_browsing_tab_logo.png')
        private_content_blocking_warning_pattern = Pattern('private_window_content_blocking_warning.png')
        info_button_pattern = Pattern('info_button.png')
        open_trackers_list_pattern = Pattern('trackers_button.png')
        trackers_list_header_pattern = Pattern('trackers_list_header.png')
        list_of_page_trackers_pattern = Pattern('list_of_page_trackers.png')
        to_block_set_to_strict_pattern = Pattern('to_block_set_to_strict.png')


        new_tab()
        navigate('about:preferences#privacy')
        navigated_to_preferences = exists(privacy_page_pattern, 10)
        assert_true(self, navigated_to_preferences,
                    'The about:preferences#privacy page is successfully displayed.')

        custom_radio_found = exists(custom_privacy_radio_pattern)
        assert_true(self, custom_radio_found,
                    'Custom" radio button from the "Content Blocking" section is displayed .')
        click(custom_privacy_radio_pattern)

        custom_protection_popup_opened = exists(trackers_checked_pattern)
        assert_true(self, custom_protection_popup_opened,
                    'The Custom panel is unfolded.')

        click(trackers_unchecked_pattern)
        hover(Location(SCREEN_WIDTH, SCREEN_HEIGHT / 2), duration=0.5)
        content_blocking_trackers_unchecked = exists(trackers_unchecked_pattern)
        assert_true(self, content_blocking_trackers_unchecked,
                    'The trackers checkbox is unchecked successfully.')

        close_tab()

        new_tab()
        navigate('http://edition.cnn.com')
        cnn_logo_exists = exists(cnn_logo_pattern, 80)
        assert_true(self, cnn_logo_exists,
                    'The website is successfully displayed.')

        tracking_protection_shield_common_window = exists(tracking_protection_shield_pattern, timeout=10)
        assert_true(self, tracking_protection_shield_common_window,
                    'The Content blocking shield is displayed near the address bar.')

        new_private_window()
        private_window_opened = exists(private_browsing_tab_pattern)
        assert_true(self, private_window_opened,
                    'Private browsing window opened')

        content_blocking_private_not_displayed = not exists(private_content_blocking_warning_pattern)
        assert_true(self, content_blocking_private_not_displayed,
                    '\'Some websites use trackers that can monitor your activity\' etc. not displayed')

        navigate('http://edition.cnn.com')
        cnn_logo_exists = exists(cnn_logo_pattern, 80)
        assert_true(self, cnn_logo_exists,
                    'The website is successfully displayed.')

        tracking_protection_shield_private_window = exists(tracking_protection_shield_pattern, timeout=10)
        assert_true(self, tracking_protection_shield_private_window,
                    'The Content blocking shield is displayed near the address bar in private window')

        info_button_located = exists(info_button_pattern)
        assert_true(self, info_button_located, 'The "i button" (Info button) is located near the address bar')
        click(info_button_pattern)

        open_trackers_list_button_located = exists(open_trackers_list_pattern)
        assert_true(self, open_trackers_list_button_located,
                    'The site information panel is displayed.')
        click(open_trackers_list_pattern)
        hover(Location(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        trackers_list_header_located = exists(trackers_list_header_pattern)
        assert_true(self, trackers_list_header_located,
                    'The trackers are not blocked.')
        click(trackers_list_header_located, DEFAULT_UI_DELAY)

        list_of_page_trackers_located = exists(list_of_page_trackers_pattern, 5)
        assert_true(self, list_of_page_trackers_located, 'The list of all page trackers is displayed.')

        to_block_set_to_strict_located = exists(to_block_set_to_strict_pattern, 5)
        assert_true(self, to_block_set_to_strict_located, 'To block all trackers, set content blocking to "Strict" is displayed')

        close_window()
