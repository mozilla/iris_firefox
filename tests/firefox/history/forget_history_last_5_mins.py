# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Forget all the history from the last 5 minutes.',
        locale=['en-US'],
        test_case_id='174072',
        test_suite_id='2000'
    )
    def run(self, firefox):
        forget_customize_page_pattern = Pattern('forget_customize_page.png')
        forget_toolbar_pattern = Pattern('forget_toolbar.png')
        forget_button_pattern = History.ForgetLast.FORGET_BUTTON
        five_minutes_selected_pattern = History.ForgetLast.LAST_FIVE_MINUTES_SELECTED
        toolbar_pattern = NavBar.TOOLBAR
        recent_history_cleared_pattern = History.ForgetLast.SUCCESS_FORGET_MSG
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY

        # Open a page to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected, 'Mozilla page successfully loaded.'

        # Open the History sidebar and make sure that 'Today' history button exists.
        history_sidebar()

        expected = exists(history_today_sidebar_pattern, 10)
        assert expected, 'Expand history button for \'Today\' history is displayed properly.'

        click_hamburger_menu_option('Customize...')

        expected = exists(forget_customize_page_pattern, 10)
        assert expected, 'Forget pattern found in the \'Customize\' page.'

        drag_drop(forget_customize_page_pattern, toolbar_pattern, duration=0.5)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        previous_tab()

        expected = exists(forget_toolbar_pattern, 10)
        assert expected, 'Forget pattern found in toolbar.'

        click(forget_toolbar_pattern)

        expected = exists(five_minutes_selected_pattern, 10)
        assert expected, 'The Forget menu is displayed with the Five minutes option selected by default.'

        expected = exists(forget_button_pattern, 10)
        assert expected, 'Forget button found.'

        click(forget_button_pattern)

        try:
            expected = wait_vanish(history_today_sidebar_pattern, 10)
            assert expected, 'Expand history button for \'Today\' history is successfully removed.'
        except FindError:
            raise FindError('Expand history button for \'Today\' history is not removed.')

        expected = exists(recent_history_cleared_pattern, 10)
        assert expected, 'Recent history successfully cleared.'
