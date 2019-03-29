# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '[Avast] Page loads should not stall - 1373365.'
        self.test_case_id = '217869'
        self.test_suite_id = '3063'
        self.locales = ['en-US']

    def run(self):
        site_logo_pattern = Pattern('kitely_logo.png')
        site_content_pattern = Pattern('kitely_content.png')

        navigate('https://www.kitely.com/')
        site_logo_exists = exists(site_logo_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, site_logo_exists, 'Logo is loaded properly')

        site_content_exists = exists(site_content_pattern)
        assert_true(self, site_content_exists, 'Page loads properly, there\'s no obvious stall')

