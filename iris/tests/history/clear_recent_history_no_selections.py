# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'No sections selected in Clear Recent History window.'
        self.test_case_id = '172046'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def run(self):
        clear_recent_history_window = Pattern('clear_recent_history_window.png')
        clear_now_button_disabled = Pattern('clear_now_button_disabled.png')
        clear_history_dialog_box_browsing = Pattern('clear_history_browsing.png')
        clear_history_dialog_box_cache = Pattern('clear_history_cache.png')
        clear_history_dialog_box_cookies = Pattern('clear_history_cookies.png')
        clear_history_dialog_box_form = Pattern('clear_history_form.png')
        clear_history_dialog_box_logins = Pattern('clear_history_logins.png')

        # Open some pages to create some history.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_1, 'Mozilla page loaded successfully.')

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        expected_2 = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected_2, 'Firefox page loaded successfully.')

        # Open the History sidebar.
        history_sidebar()

        # Open the 'Clear Recent History' window and uncheck all the items.
        clear_recent_history()
        expected_3 = exists(clear_recent_history_window, 10)
        assert_true(self, expected_3, 'Clear Recent History window was displayed properly.')

        pref_list = [clear_history_dialog_box_logins, clear_history_dialog_box_browsing,
                     clear_history_dialog_box_cache, clear_history_dialog_box_cookies,
                     clear_history_dialog_box_form]
        for image in pref_list:
            if exists(image, 10):
                click(image)

        # Check that the 'Clear Now' button is disabled.
        expected_4 = exists(clear_now_button_disabled.similar(0.9), 10)
        assert_true(self, expected_4, 'Clear Now button is disabled.')

        # Close the 'Clear Recent History' window.
        type(Key.ESC)
