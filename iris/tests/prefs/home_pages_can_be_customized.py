# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Home pages can be customized'
        self.test_case_id = '161463'
        self.test_suite_id = '2241'
        self.locales = ['en-US']

    def run(self):
        custom_url_option_pattern = Pattern('custom_url_option.png')
        default_new_tab_setting_home_pattern = Pattern('default_new_tab_setting_home.png')
        homepage_new_windows_pattern = Pattern('homepage_new_windows.png')
        url_field_pattern = Pattern('url_field.png')

        navigate('about:preferences#home')
        preferences_are_opened = exists(homepage_new_windows_pattern)
        assert_true(self, preferences_are_opened, 'Preferences#Home page is opened')

        preference_region_offset = homepage_new_windows_pattern.get_size()[1]
        preference_location = find(homepage_new_windows_pattern)
        preference_region = Region(preference_location.x, preference_location.y - (preference_region_offset // 2),
                                   SCREEN_WIDTH // 2, preference_region_offset * 2)

        home_is_default = exists(default_new_tab_setting_home_pattern, in_region=preference_region)
        assert_true(self, home_is_default, 'Preferences page is opened, Firefox Home is set as default ')

        click(default_new_tab_setting_home_pattern, in_region=preference_region)

        custom_url_option_exists = exists(custom_url_option_pattern)
        assert_true(self, custom_url_option_exists, '"Custom URL" option is displayed')

        click(custom_url_option_pattern)

        url_field_displayed = exists(url_field_pattern)
        assert_true(self, url_field_displayed, 'URL field is displayed')

        click(url_field_pattern)

        paste(LocalWeb.FIREFOX_TEST_SITE)

        type(Key.ENTER)

        restart_firefox(self, self.browser.path, self.profile_path, self.base_local_web_url)

        new_window()
        custom_webpage_displayed_as_default_in_new_window = exists(LocalWeb.FIREFOX_LOGO)
        assert_true(self, custom_webpage_displayed_as_default_in_new_window, 'Custom page was set as default')

        close_tab()
