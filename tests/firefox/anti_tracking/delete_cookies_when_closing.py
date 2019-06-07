# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox can be set to delete cookies when closed.',
        locale=['en-US'],
        test_case_id='106157',
        test_suite_id='1826'
    )
    def run(self, firefox):
        preferences_privacy_page_pattern = AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED
        delete_cookies_after_close_pattern = Pattern('delete_cookies_after_close.png')
        delete_cookies_after_close_marked_pattern = Pattern('delete_cookies_after_close_marked.png')
        manage_data_button_pattern = Pattern('manage_data_button.png')
        prosport_cookies_pattern = Pattern('prosport_cookies.png')
        manage_cookies_window_label_pattern = Pattern('manage_cookies_window_label.png')

        navigate('about:preferences#privacy')

        preferences_privacy_page_opened = exists(preferences_privacy_page_pattern,
                                                 FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert preferences_privacy_page_opened, 'The Preferences > Privacy page is successfully displayed'

        paste('Delete cookies')

        delete_cookies_after_close_checkbox_exists = exists(delete_cookies_after_close_pattern)
        assert delete_cookies_after_close_checkbox_exists, '"Delete cookies and site data when Firefox is closed" ' \
                                                           'is displayed'

        delete_cookies_after_close_location = find(delete_cookies_after_close_pattern)
        delete_cookies_checkbox_width, delete_cookies_checkbox_height = delete_cookies_after_close_pattern.get_size()
        delete_cookies_region = Rectangle(delete_cookies_after_close_location.x, delete_cookies_after_close_location.y,
                                          delete_cookies_checkbox_width, delete_cookies_checkbox_height)

        click(delete_cookies_after_close_pattern)

        delete_cookies_after_close_marked_exists = exists(delete_cookies_after_close_marked_pattern,
                                                          region=delete_cookies_region)
        assert delete_cookies_after_close_marked_exists, 'The option is successfully selected and remembered.'

        new_tab()

        navigate('https://edition.cnn.com')

        website_opened = exists(LocalWeb.CNN_LOGO, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert website_opened, 'The website is successfully displayed.'

        close_tab()

        firefox.restart(url='about:preferences#privacy', image=preferences_privacy_page_pattern)

        time.sleep(FirefoxSettings.FIREFOX_TIMEOUT)

        open_find()

        paste('Delete cookies')

        manage_data_button_exists = exists(manage_data_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert manage_data_button_exists, 'The manage data button exists.'

        click(manage_data_button_pattern)

        manage_cookies_window_exists = exists(manage_cookies_window_label_pattern)
        assert manage_cookies_window_exists, 'The manage data button exists.'

        paste('cnn')

        cookies_is_not_saved = exists(prosport_cookies_pattern)
        assert cookies_is_not_saved, 'No cookies are displayed from the previously accessed website.'
