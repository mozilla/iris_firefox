# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open a website in the current tab and then check it is displayed in the Recent History list.',
        locale=['en-US'],
        test_case_id='118800',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        recent_history_mozilla_pattern = Pattern('recent_history_mozilla.png')

        # Open a website in the current tab.
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_1 is True, 'Mozilla page loaded successfully.'

        # Check that the previously opened page is displayed on the top of the Recent History list.
        open_library_menu('History')

        expected_2 = exists(recent_history_mozilla_pattern, 10)
        assert expected_2 is True, 'Mozilla page displayed in the History list successfully.'
