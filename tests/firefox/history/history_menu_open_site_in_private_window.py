# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open a website from the Recent History list in a private window.',
        locale=['en-US'],
        test_case_id='118808',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        recent_history_mozilla_pattern = LocalWeb.MOZILLA_BOOKMARK

        # Open a page to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_1, 'Mozilla page loaded successfully.'

        # Click on a page from the History list in a private window.
        new_private_window()
        open_library_menu('History')

        right_upper_corner = Screen().new_region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2,
                                                 Screen.SCREEN_HEIGHT / 2)

        expected_2 = right_upper_corner.exists(recent_history_mozilla_pattern, 10)
        assert expected_2, 'Mozilla page displayed in the History list successfully.'

        right_upper_corner.click(recent_history_mozilla_pattern)

        # Check that the page was opened successfully.
        expected_3 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_3, 'Mozilla page loaded successfully.'
