# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bug 1357098 - Pinned tabs are not restored after browser restart.'
        self.test_case_id = '114816'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def run(self):
        focus_tab_pattern = Pattern('focus_tab.png')
        focus_pinned_tab_pattern = Pattern('focus_pinned_tab.png')
        firefox_tab_pattern = Pattern('firefox_tab.png')
        firefox_pinned_tab_pattern = Pattern('firefox_pinned_tab.png')

        pin_tab = 3

        navigate(LocalWeb.FOCUS_TEST_SITE)

        focus_site_opened = exists(LocalWeb.FOCUS_LOGO, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, focus_site_opened, 'Focus website is properly opened.')

        focus_tab_exists = exists(focus_tab_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, focus_tab_exists, 'Focus tab is available.')

        right_click(focus_tab_pattern)

        repeat_key_down(pin_tab)
        type(Key.ENTER)

        focus_tab_pinned = exists(focus_pinned_tab_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, focus_tab_pinned, 'Focus tab successfully pinned.')

        new_window()

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        firefox_test_site_opened = exists(LocalWeb.FIREFOX_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, firefox_test_site_opened, 'Firefox website is properly opened.')

        firefox_test_tab_exists = exists(firefox_tab_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, firefox_test_tab_exists, 'Firefox tab is available.')

        right_click(firefox_tab_pattern)

        repeat_key_down(pin_tab)
        type(Key.ENTER)

        firefox_test_tab_pinned = exists(firefox_pinned_tab_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, firefox_test_tab_pinned, 'Firefox tab successfully pinned.')

        restart_firefox(self, self.browser.path, self.profile_path, self.base_local_web_url, image=LocalWeb.IRIS_LOGO)

        close_tab()

        firefox_test_tab_pinned = exists(firefox_pinned_tab_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, firefox_test_tab_pinned, 'Firefox tab is pinned after restart.')

        close_window()

        focus_tab_pinned = exists(focus_pinned_tab_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, focus_tab_pinned, 'Focus tab is pinned after restart.')

        assert_true(self, firefox_test_tab_pinned and focus_tab_pinned,
                    'Browser starts with two windows. Both "example.com" and "example.org" are pinned and available in '
                    'respective windows.\n\n Note: old builds affected by this bug have shown this behavior: "Browser '
                    'started with two windows. Only "example.com" pinned tab has been restored in its window. Second '
                    'window contains two blank tabs. "example.org" pinned tab has been lost."')
