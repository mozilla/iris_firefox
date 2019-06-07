# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open the History Menu and check the Recent History list.',
        locale=['en-US'],
        test_case_id='118799',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        recent_history_default_pattern = Pattern('recent_history_default.png')

        # Open the History Menu and check the Recent History list.
        open_library_menu('History')

        expected = exists(recent_history_default_pattern, 10)
        assert expected, 'The expected items are displayed in the History list.'
