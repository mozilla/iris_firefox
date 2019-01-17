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
        preferences_privacy_page_pattern = Pattern('preferences_privacy_icon.png')
        delete_cookies_after_close_pattern = Pattern('delete_cookies_after_close.png')
        delete_cookies_after_close_marked_pattern = Pattern('delete_cookies_after_close_marked.png')
        prosport_opened_mark_pattern = Pattern('prosport_opened_mark.png')
        manage_data_button_pattern = Pattern('manage_data_button.png')
        prosport_cookies_pattern = Pattern('prosport_cookies.png')
        manage_cookies_window_label_pattern = Pattern('manage_cookies_window_label.png')

        navigate('about:preferences#privacy')
        time.sleep(6)

        preferences_privacy_page_pattern = exists(preferences_privacy_page_pattern, 30)
        assert_true(self, preferences_privacy_page_pattern, 'The Preferences > Privacy page is successfully displayed')

        type('Delete cookies')

        delete_cookies_after_close_checkbox_exists = exists(delete_cookies_after_close_pattern)
        assert_true(self, delete_cookies_after_close_checkbox_exists, '"Delete cookies and site data when Firefox '
                                                                      'is closed" is displayed')
        click(delete_cookies_after_close_pattern)

        delete_cookies_after_close_marked_exists = exists(delete_cookies_after_close_marked_pattern)
        assert_true(self, delete_cookies_after_close_marked_exists, 'The option is successfully selected and '
                                                                    'remembered.')

        navigate('http://www.prosport.ro/')

        prosport_opened_mark = exists(prosport_opened_mark_pattern, 100)
        assert_true(self, prosport_opened_mark, 'The website is successfully displayed.')

        quit_firefox()

        self.firefox_runner = launch_firefox(
            self.browser.path,
            self.profile_path,
            url='about:preferences#privacy')
        self.firefox_runner.start()

        wait_for_firefox_restart()

        maximize_window()
        type('closed')

        time.sleep(5)

        manage_data_button_exists = exists(manage_data_button_pattern)
        assert_true(self, manage_data_button_exists, 'The manage data button exists.')

        click(manage_data_button_pattern)

        manage_cookies_window_exists= exists(manage_cookies_window_label_pattern)
        assert_true(self, manage_cookies_window_exists, 'The manage data button exists.')

        type('prosport')

        prosport_cookies_is_not_saved = exists(prosport_cookies_pattern)
        assert_true(self, prosport_cookies_is_not_saved, 'No cookies are displayed from the previously accessed '
                                                         'website.')













