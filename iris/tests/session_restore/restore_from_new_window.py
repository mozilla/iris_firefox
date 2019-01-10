# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Session restore can be performed from a new window'
        self.test_case_id = 'C117040'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW

    def run(self):
        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        website_one_loaded = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, website_one_loaded,
                    'Page 1 successfully loaded, firefox logo found.')

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        website_two_loaded = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, website_two_loaded,
                    'Page 2 successfully loaded, mozilla logo found.')

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        self.base_local_web_url)

        click_hamburger_menu_option('Restore Previous Session')

        select_tab(5)
        website_one_loaded = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, website_one_loaded,
                    'Page 1 successfully restored from previous session.')

        select_tab(4)
        website_two_loaded = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, website_two_loaded,
                    'Page 2 successfully restored from previous session.')
