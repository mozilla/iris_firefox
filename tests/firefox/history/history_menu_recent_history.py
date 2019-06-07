# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Page visits show in Recent history.',
        locale=['en-US'],
        test_case_id='178345',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        # Open some pages to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_1, 'Mozilla page loaded successfully.'

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        expected_2 = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected_2, 'Firefox page loaded successfully.'

        navigate(LocalWeb.FOCUS_TEST_SITE)

        expected_3 = exists(LocalWeb.FOCUS_LOGO, 10)
        assert expected_3, 'Focus page loaded successfully.'

        navigate(LocalWeb.POCKET_TEST_SITE)

        expected_4 = exists(LocalWeb.POCKET_LOGO, 10)
        assert expected_4, 'Pocket page loaded successfully.'

        # Open History and check if is populated with the recent visited websites.
        open_library_menu('History')
        right_upper_corner = Screen().new_region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2,
                                                 Screen.SCREEN_HEIGHT / 2)

        expected_5 = right_upper_corner.exists(LocalWeb.POCKET_BOOKMARK, 10)
        assert expected_5, 'Pocked is displayed.'

        expected_6 = exists(LocalWeb.MOZILLA_BOOKMARK, 10)
        assert expected_6, 'Mozilla page displayed Recent History list successfully.'

        expected_7 = exists(LocalWeb.FIREFOX_BOOKMARK, 10)
        assert expected_7, 'Firefox is displayed.'

        expected_8 = exists(LocalWeb.FOCUS_BOOKMARK, 10)
        assert expected_8, 'Focus is displayed.'

        type(Key.ESC)
