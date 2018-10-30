# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case checks that navigation to a page without entering the \'http://\' protocol works ' \
                    'correctly.'
        self.test_case_id = '117529'
        self.test_suite_id = '1902'
        self.locales = ['en-US', 'zh-CN', 'es-ES', 'fr', 'de', 'ar', 'ru', 'ko', 'pt-PT', 'vi', 'pl', 'tr', 'ro', 'ja']

    def run(self):
        apache_logo_pattern = Pattern('apache_logo.png')

        navigate('httpd.apache.org')

        expected = exists(apache_logo_pattern, 10)
        assert_true(self, expected, 'Page successfully loaded, Apache logo found.')
