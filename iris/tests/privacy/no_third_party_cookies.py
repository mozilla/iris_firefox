# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Firefox can be set to never remember browsing history."
        self.test_case_id = "106156"
        self.test_suite_id = "1956"
        self.locale = ["en-US"]

    def run(self):
        block_all_third_party_cookies_pattern = Pattern('block_all_third_party_cookies.png')
        cookies_blocking_strictness_menu_pattern = Pattern('cookies_blocking_strictness_menu.png')
        cookies_ticked_pattern = Pattern('block_cookies_ticked.png')
        cookies_unticked_pattern = Pattern('block_cookies_unticked.png')
        custom_content_blocking_pattern = Pattern('custom_content_blocking_unticked.png')
        site_tab = Pattern('prosport_tab.png')

        new_tab()
        navigate('about:preferences#privacy')
        preferences_opened = exists(custom_content_blocking_pattern)
        assert_true(self, preferences_opened, 'The page is successfully displayed.')

        click(custom_content_blocking_pattern)
        options_displayed = exists(cookies_unticked_pattern)
        assert_true(self, options_displayed, 'The options are properly displayed.')

        click(cookies_unticked_pattern)
        checkbox_set_successfully = exists(cookies_ticked_pattern)
        assert_true(self, checkbox_set_successfully, 'The checkbox is successfully set.')

        strictness_menu_appeared = exists(cookies_blocking_strictness_menu_pattern)
        assert_true(self, strictness_menu_appeared, 'Strictness menu appeared.')

        click(cookies_blocking_strictness_menu_pattern)
        strictness_dropdown_displayed = exists(block_all_third_party_cookies_pattern)
        assert_true(self, strictness_dropdown_displayed, 'Cookies blocking dropdown menu displayed.')

        click(block_all_third_party_cookies_pattern)

        navigate('http://www.prosport.ro/')
        site_loaded = exists(site_tab, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, site_loaded, 'The "Prosport" website is successfully displayed.')

        navigate('about:preferences#privacy')
        preferences_opened = exists(custom_content_blocking_pattern)
        assert_true(self, preferences_opened, 'The page is successfully displayed.')

