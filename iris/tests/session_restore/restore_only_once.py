# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Firefox can be set to restore a session only once'
        self.test_case_id = '115423'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def run(self):
        url_first = LocalWeb.FIREFOX_TEST_SITE
        url_second = LocalWeb.FIREFOX_TEST_SITE_2

        change_preference('browser.sessionstore.resume_session_once', 'true')

        new_tab()
        navigate(url_first)
        website_one_loaded = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, website_one_loaded, 'Page 1 successfully loaded, firefox logo found.')

        new_tab()
        navigate(url_second)
        website_two_loaded = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, website_two_loaded, 'Page 2 successfully loaded, firefox logo found.')

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        self.base_local_web_url)

        previous_tab()
        website_one_loaded = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, website_one_loaded, 'Page 1 successfully loaded after restart.')

        previous_tab()
        website_two_loaded = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, website_two_loaded, 'Page 2 successfully loaded after restart.')
        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        self.base_local_web_url)

        previous_tab()
        website_one_loaded = exists(LocalWeb.FIREFOX_LOGO, 1)
        assert_false(self, website_one_loaded, 'Page 1 was not loaded after second restart.')

        previous_tab()
        website_two_loaded = exists(LocalWeb.FIREFOX_LOGO, 1)
        assert_false(self, website_two_loaded, 'Page 2 was not loaded after second restart.')
