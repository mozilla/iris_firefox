# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Previously closed tabs can be restored by using keyboard combinations'
        self.test_case_id = '117047'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def run(self):
        local_url = [LocalWeb.FIREFOX_TEST_SITE, LocalWeb.FIREFOX_TEST_SITE_2, LocalWeb.FOCUS_TEST_SITE,
                     LocalWeb.FOCUS_TEST_SITE_2, LocalWeb.MOZILLA_TEST_SITE]
        local_url_logo_pattern = [LocalWeb.FIREFOX_LOGO, LocalWeb.FIREFOX_LOGO, LocalWeb.FOCUS_LOGO,
                                  LocalWeb.FOCUS_LOGO, LocalWeb.MOZILLA_LOGO]

        for _ in range(5):
            new_tab()
            navigate(local_url[_])
            website_loaded = exists(local_url_logo_pattern[_], 20)
            assert_true(self, website_loaded,
                        'Website {0} loaded'
                        .format(_ + 1))

        [close_tab() for _ in range(4)]

        one_tab_exists = exists(local_url_logo_pattern[0], 20)
        assert_true(self, one_tab_exists,
                    'One opened tab left. {0} tabs were successfully closed.'
                    .format(len(local_url) - 1))

        for _ in range(4):
            undo_close_tab()
            tab_is_restored = exists(local_url_logo_pattern[_+1])  # +1 as url[0] is one opened tab
            assert_true(self, tab_is_restored,
                        'Tab {0} successfully restored'
                        .format(_ + 2))
