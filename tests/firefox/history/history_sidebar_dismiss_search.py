# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Dismiss the search from the History sidebar.',
        locale=['en-US'],
        test_case_id='119442',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        history_sidebar_focus_pattern = Pattern('history_sidebar_focus.png').similar(0.7)
        search_history_box_pattern = Sidebar.HistorySidebar.SEARCH_BOX
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        x_button_search_history_box_pattern = Sidebar.SidebarHeader.CLEAR_SEARCH_BOX
        history_sidebar_items_pattern = Pattern('history_sidebar_items.png')

        if OSHelper.is_windows():
            x_button_search_history_box_pattern = Pattern('x_button_search_history.png')

        # Open a page to create some history.
        navigate(LocalWeb.FOCUS_TEST_SITE)

        focus_logo_exists = exists(LocalWeb.FOCUS_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert focus_logo_exists, 'Focus page loaded successfully.'

        # Open the History sidebar.
        history_sidebar()

        search_history_box_exists = exists(search_history_box_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert search_history_box_exists, 'History Sidebar is opened.'

        history_today_sidebar_exists = exists(history_today_sidebar_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert history_today_sidebar_exists, 'Expand history button displayed properly.'

        click(history_today_sidebar_pattern)
        click(search_history_box_pattern)

        # Check that Focus page is found in the History list.
        paste('focus')
        type(Key.TAB)

        history_sidebar_focus_exists = exists(history_sidebar_focus_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                              region=Screen().top_half().left_third())
        assert history_sidebar_focus_exists, 'Focus page was found in the History list successfully.'

        # Clear the History search box.
        x_button_search_history_box_exists = exists(x_button_search_history_box_pattern,
                                                    FirefoxSettings.FIREFOX_TIMEOUT)
        assert x_button_search_history_box_exists, 'Clear field button was displayed properly.'

        click(x_button_search_history_box_pattern)

        history_sidebar_items_exists = exists(history_sidebar_items_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert history_sidebar_items_exists, 'History sidebar item exists'

        search_history_box_exists = exists(search_history_box_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert search_history_box_exists, 'The search field is empty and all the History is displayed below.'
