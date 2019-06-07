# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='[Avast] Page loads should not stall - 1373365.',
        locale=['en-US'],
        test_case_id='217869',
        test_suite_id='3063'
    )
    def run(self, firefox):
        site_logo_pattern = Pattern('kitely_logo.png')
        site_content_pattern = Pattern('kitely_content.png')

        navigate('https://www.kitely.com/')
        assert exists(site_logo_pattern, 10), 'Logo is loaded properly.'

        close_content_blocking_pop_up()
        assert exists(site_content_pattern), 'Page loads properly, there\'s no obvious stall.'

