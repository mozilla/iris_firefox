# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case checks that url bar properly unescapes ASCII url.'
        self.test_case_id = '118809'
        self.test_suite_id = '1902'
        self.locales = ['en-US', 'zh-CN', 'es-ES', 'fr', 'de', 'ar', 'ru', 'ko', 'pt-PT', 'vi', 'pl', 'tr', 'ro', 'ja']

    def run(self):
        url_example_pattern = Pattern('url_example.png')

        navigate('data:text/html,<a href="http://example.org/?q">Link</a>')

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        expected = region.exists(url_example_pattern, 10)
        assert_true(self, expected, 'The url remains unchanged.')
