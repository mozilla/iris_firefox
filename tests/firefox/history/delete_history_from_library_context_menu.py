# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Delete history from Library context menu',
        locale=['en-US'],
        test_case_id='178346',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        history_mozilla_pattern = Pattern('library_bookmarks_mozilla.png')
        history_pattern = Library.HISTORY
        history_today_pattern = Library.HISTORY_TODAY

        # Open a page to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_1, 'Mozilla page loaded successfully.'

        # Open History.
        open_library()

        expected_2 = exists(history_pattern, 10)
        assert expected_2, 'History section is displayed.'

        # Expand History.
        double_click(history_pattern)

        expected_3 = exists(history_today_pattern.similar(0.6), 10)
        assert expected_3, 'Today history option is available.'

        # Verify if Mozilla page is present in Today History.
        Mouse().move(Location(Screen.SCREEN_WIDTH / 4 + 100, Screen.SCREEN_HEIGHT / 4))
        double_click(history_today_pattern)

        expected_4 = exists(history_mozilla_pattern, 10)
        assert expected_4, 'Mozilla page is displayed in the History list successfully.'

        # Delete Mozilla page from Today's History.
        right_click_and_type(history_mozilla_pattern, keyboard_action='d')

        try:
            expected_5 = wait_vanish(history_mozilla_pattern.similar(0.9), 10)
            assert expected_5, 'Mozilla page was deleted successfully from the history.'
        except FindError:
            raise FindError('Mozilla page is still displayed in the history.')

        click_window_control('close')
