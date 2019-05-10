
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Firefox can be set to display the home page on launch'
        self.test_case_id = '143543'
        self.test_suite_id = '2241'
        self.locales = ['en-US']

    def run(self):
        default_new_tab_setting_home_pattern = Pattern('default_new_tab_setting_home.png')
        homepage_new_windows_pattern = Pattern('homepage_new_windows.png')

        navigate('about:preferences#home')

        preferences_opened = exists(default_new_tab_setting_home_pattern)
        assert_true(self, preferences_opened, 'Preferences is opened')

        new_page_is_firefox_home = exists(homepage_new_windows_pattern)
        assert_true(self, new_page_is_firefox_home, 'Firefox home page was set as default new page')

        restart_firefox(self, self.browser.path, self.profile_path, '', image=Tabs.NEW_TAB_HIGHLIGHTED)

        new_tab_opened = exists(Tabs.NEW_TAB_HIGHLIGHTED, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, new_tab_opened, 'Browser was opened with firefox homepage')

        new_tab_content_displayed = exists(Utils.TOP_SITES)
        assert_true(self, new_tab_content_displayed, 'New tab content was successfully rendered.')
