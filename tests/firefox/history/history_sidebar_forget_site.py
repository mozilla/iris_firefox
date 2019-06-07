# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Forget a page from the History sidebar.',
        locale=['en-US'],
        test_case_id='120132',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        search_history_box_pattern = Sidebar.HistorySidebar.SEARCH_BOX
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY

        left_upper_corner = Screen().new_region(0, 0, Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT / 2)

        # Open a page to create some history.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_1, 'Mozilla page loaded successfully.'
        close_tab()

        # Open the History sidebar.
        history_sidebar()

        expected_2 = exists(search_history_box_pattern, 10)
        assert expected_2, 'Sidebar was opened successfully.'

        expected_3 = exists(history_today_sidebar_pattern, 10)
        assert expected_3, 'Expand history button displayed properly.'

        click(history_today_sidebar_pattern)

        # Forget a page from the History sidebar.
        expected_4 = left_upper_corner.exists(LocalWeb.MOZILLA_BOOKMARK_SMALL.similar(0.7), 10)
        assert expected_4, 'Mozilla page is displayed in the History list successfully.'

        right_click_and_type(LocalWeb.MOZILLA_BOOKMARK_SMALL, keyboard_action='f')

        try:
            expected_5 = left_upper_corner.wait_vanish(LocalWeb.MOZILLA_BOOKMARK_SMALL, 10)
            assert expected_5, 'Mozilla page was deleted successfully from the history.'
        except FindError:
            raise FindError('Mozilla page is still displayed in the history.')

        # Check that Mozilla page is not displayed in the Recent History list.
        open_library_menu('History')

        expected_6 = exists(LocalWeb.MOZILLA_BOOKMARK_SMALL.similar(0.9), 10)
        assert expected_6 is not True, 'Mozilla page is not displayed in the Recent History list.'
