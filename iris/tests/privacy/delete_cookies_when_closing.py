# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Firefox can be set to delete cookies when closed."
        self.test_case_id = "106157"
        self.test_suite_id = "1956"
        self.locale = ["en-US"]

    def run(self):
        preferences_privacy_page_pattern = AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED
        delete_cookies_after_close_pattern = Pattern('delete_cookies_after_close.png')
        delete_cookies_after_close_marked_pattern = Pattern('delete_cookies_after_close_marked.png')
        manage_data_button_pattern = Pattern('manage_data_button.png')
        prosport_cookies_pattern = Pattern('prosport_cookies.png')
        manage_cookies_window_label_pattern = Pattern('manage_cookies_window_label.png')

        navigate('about:preferences#privacy')

        preferences_privacy_page_opened = exists(preferences_privacy_page_pattern, 30)
        assert_true(self, preferences_privacy_page_opened, 'The Preferences > Privacy page is successfully displayed')

        paste('Delete cookies')

        delete_cookies_after_close_checkbox_exists = exists(delete_cookies_after_close_pattern)
        assert_true(self, delete_cookies_after_close_checkbox_exists, '"Delete cookies and site data when Firefox '
                                                                      'is closed" is displayed')
        click(delete_cookies_after_close_pattern)

        delete_cookies_after_close_marked_exists = exists(delete_cookies_after_close_marked_pattern)
        assert_true(self, delete_cookies_after_close_marked_exists, 'The option is successfully selected and '
                                                                    'remembered.')

        navigate('https://edition.cnn.com')

        website_opened = exists(LocalWeb.CNN_LOGO, 100)
        assert_true(self, website_opened, 'The website is successfully displayed.')

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        'about:preferences#privacy',
                        image=preferences_privacy_page_pattern
                        )

        time.sleep(DEFAULT_UI_DELAY)
        paste('Delete cookies')

        manage_data_button_exists = exists(manage_data_button_pattern, 10)
        assert_true(self, manage_data_button_exists, 'The manage data button exists.')

        click(manage_data_button_pattern)

        manage_cookies_window_exists = exists(manage_cookies_window_label_pattern)
        assert_true(self, manage_cookies_window_exists, 'The manage data button exists.')

        paste('cnn')

        cookies_is_not_saved = exists(prosport_cookies_pattern)
        assert_true(self, cookies_is_not_saved, 'No cookies are displayed from the previously accessed '
                                                'website.')
