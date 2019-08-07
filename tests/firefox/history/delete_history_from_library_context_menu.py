# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1385883 - Cannot delete history with IDN',
        locale=['en-US'],
        test_case_id='178346',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        mozilla_bookmark_focus_pattern = Pattern('mozilla_bookmark_focus.png')
        history_pattern = Library.HISTORY
        history_today_pattern = Library.HISTORY_TODAY

        # Open a page to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_1, 'Mozilla page loaded successfully.'

        # 3. Open the Library (Ctrl+Shift+B) and go to History section.
        open_library()

        expected_2 = exists(history_pattern, 10)
        assert expected_2, 'History section is displayed.'

        # 4. Open the Today section from History and right click on the opened website from step two.
        double_click(history_pattern)

        expected_3 = exists(history_today_pattern.similar(0.6), 10)
        assert expected_3, 'Today history option is available.'

        Mouse().move(Location(Screen.SCREEN_WIDTH / 4 + 100, Screen.SCREEN_HEIGHT / 4))
        double_click(history_today_pattern)

        # 5. Click on Delete Page button.
        # The page is correctly deleted from the list.
        # Note that the website was not deleted on the affected builds.

        expected_4 = exists(mozilla_bookmark_focus_pattern, 100)
        assert expected_4, 'Mozilla page is displayed in the History list successfully.'

        right_click_and_type(mozilla_bookmark_focus_pattern, keyboard_action='d', delay=FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)

        try:
            expected_5 = wait_vanish(mozilla_bookmark_focus_pattern.similar(0.9), 10)
            assert expected_5, 'Mozilla page was deleted successfully from the history.'
        except FindError:
            raise FindError('Mozilla page is still displayed in the history.')

        click_window_control('close')
