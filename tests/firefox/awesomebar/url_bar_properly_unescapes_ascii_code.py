# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case checks that url bar properly unescapes ASCII url.',
        locale=['en-US', 'zh-CN', 'es-ES', 'fr', 'de', 'ar', 'ru', 'ko', 'pt-PT', 'vi', 'pl', 'tr', 'ro', 'ja'],
        test_case_id='118809',
        test_suite_id='1902'
    )
    def run(self, firefox):
        url_example_pattern = Pattern('url_example.png')

        navigate('data:text/html,<a href="http://example.org/?q">Link</a>')

        region = Region(0, 0, Screen().width, 2 * Screen().height / 3)

        expected = region.exists(url_example_pattern, 10)
        assert expected, 'The url remains unchanged.'
