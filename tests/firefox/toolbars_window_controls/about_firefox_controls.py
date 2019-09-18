# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='This is a test of the \'About Firefox\' window controls',
        locale=['en-US', 'zh-CN', 'es-ES', 'fr', 'de', 'ar', 'ru', 'ko', 'pt-PT', 'vi', 'pl', 'tr', 'ro', 'ja'],
        test_case_id='120465',
        test_suite_id='1998'
    )
    def run(self, firefox):
        firefox_in_about_pattern = Pattern('firefox_in_about.png')

        open_about_firefox()
        assert exists(firefox_in_about_pattern, 10), '\'About Firefox\' window was opened successfully.'

        click_window_control('close')
        try:
            assert wait_vanish(firefox_in_about_pattern, 10), '\'About Firefox\' window was closed successfully.'
        except FindError:
            raise FindError('About Firefox\' window is still open')
