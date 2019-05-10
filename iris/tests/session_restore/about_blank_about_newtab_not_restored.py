# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bug 1323987 - about:blank and about:newtab aren\'t restored by Session Restore'
        self.test_case_id = '116003'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def run(self):
        blank_white_squre_400_200_pattern = Pattern('blank_white_squre_400_200.png')
        middle_vertical_region = Screen.MIDDLE_THIRD_VERTICAL
        center_region = middle_vertical_region.middle_third_horizontal()

        navigate('about:newtab')
        top_sites_available = exists(Utils.TOP_SITES, Settings.FIREFOX_TIMEOUT)
        assert_true(self, top_sites_available, 'about:newtab website loaded successfully')

        new_tab()
        navigate('about:blank')
        time.sleep(Settings.TINY_FIREFOX_TIMEOUT)  # Pattern of new tab will be found before loading about:blank

        about_blank_tab = exists(blank_white_squre_400_200_pattern, Settings.TINY_FIREFOX_TIMEOUT, center_region)
        assert_true(self, about_blank_tab, 'about:blank website loaded successfully')

        restart_firefox(self, self.browser.path, self.profile_path, self.base_local_web_url,
                        image=LocalWeb.IRIS_LOGO_ACTIVE_TAB)

        click_hamburger_menu_option('Restore Previous Session')

        close_tab()

        top_sites_available = exists(Utils.TOP_SITES, Settings.TINY_FIREFOX_TIMEOUT, Screen.LEFT_HALF)
        assert_true(self, top_sites_available, 'about:newtab website restored successfully')

        next_tab()

        about_blank_tab = exists(blank_white_squre_400_200_pattern, Settings.TINY_FIREFOX_TIMEOUT, center_region)
        assert_true(self, about_blank_tab, 'about:blank website restored successfully')
