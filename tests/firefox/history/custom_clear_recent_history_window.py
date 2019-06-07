# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Custom sections selected in \'Clear Recent History\' window',
        locale=['en-US'],
        test_case_id='172047',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW,
        preferences={'datareporting.policy.firstRunURL': ''}
    )
    def run(self, firefox):
        clear_recent_history_window_pattern = History.CLearRecentHistory.CLEAR_RECENT_HISTORY_TITLE
        clear_now_button_pattern = History.CLearRecentHistory.CLEAR_NOW
        search_uncheked_box_pattern = Utils.UNCHECKEDBOX
        history_pattern = Sidebar.HistorySidebar.SIDEBAR_HISTORY_TITLE
        searched_history_logo_pattern = Sidebar.HistorySidebar.EXPLORED_HISTORY_ICON
        privacy_logo_pattern = Pattern('privacy_logo.png')
        manage_data_pattern = Pattern('manage_data_button.png')
        manage_data_title_pattern = Pattern('manage_cookies_and_site_data_table_heads.png')
        saved_logins_button_pattern = Pattern('saved_logins_button.png')
        saved_logins_window_pattern = Pattern('saved_logins_table_heads.png')
        empty_saved_logins_pattern = Pattern('empty_saved_logins.png')

        # Open the 'Clear Recent History' window and uncheck all the items.
        for step in open_clear_recent_history_window():
            assert step.resolution, step.message

        # Check all options to be cleared.
        expected = exists(search_uncheked_box_pattern.similar(0.9), 10)
        while expected:
            click(search_uncheked_box_pattern)
            time.sleep(Settings.DEFAULT_UI_DELAY)
            expected = exists(search_uncheked_box_pattern.similar(0.9), 10)

        try:
            wait(History.CLearRecentHistory.TimeRange.LAST_HOUR, 10)
            logger.debug('Last Hour option found.')
            click(History.CLearRecentHistory.TimeRange.LAST_HOUR)
        except FindError:
            raise FindError('Last Hour option NOT found, aborting')

        try:
            wait(History.CLearRecentHistory.TimeRange.EVERYTHING, 10)
            logger.debug('Everything option found.')
            click(History.CLearRecentHistory.TimeRange.EVERYTHING)
        except FindError:
            raise FindError('Everything option NOT found, aborting')

        time.sleep(Settings.DEFAULT_UI_DELAY)

        # Clear the Clear recent history.
        expected = exists(clear_now_button_pattern, 10)
        assert expected, '\"Clear Now\" button found.'

        click(clear_now_button_pattern)

        # Check that the Clear Recent History window was dismissed properly.
        expected = exists(clear_recent_history_window_pattern.similar(0.9), 10)
        assert expected is not True, 'Clear Recent History window was dismissed properly.'

        # ASSERTS.
        time.sleep(Settings.DEFAULT_UI_DELAY)
        # Open the History sidebar.
        history_sidebar()

        expected = exists(history_pattern, 10)
        assert expected, 'History sidebar is opened.'

        # Check that the history is empty.
        region = Screen().new_region(0, 150, Screen.SCREEN_WIDTH / 2,Screen.SCREEN_HEIGHT / 2)

        expected = region.exists(searched_history_logo_pattern, 10)
        assert expected is not True, 'History is empty.'

        # Close the History sidebar.
        history_sidebar()

        expected = exists(history_pattern, 10)
        assert expected is not True, 'History sidebar is closed.'

        # Check that cookies were deleted.
        # Access the privacy page.
        navigate('about:preferences#privacy')

        expected = exists(privacy_logo_pattern, 10)
        assert expected, 'Privacy page has been accessed.'

        # Scroll in page and access the "Saved Logins" button.
        Mouse().move(Location(Screen.SCREEN_WIDTH / 4 + 100, Screen.SCREEN_HEIGHT / 4))
        time.sleep(Settings.SYSTEM_DELAY)

        expected = exists(saved_logins_button_pattern, 2)
        while not expected:
            scroll_down(5, 2)
            expected = exists(saved_logins_button_pattern, 2)

        assert expected, '\"Saved Logins\" button has been found.'
        click(saved_logins_button_pattern)

        # Check that "Saved Logins" window is displayed.

        expected = exists(saved_logins_window_pattern, 10)
        assert expected, '\"Saved Logins\" window is displayed.'

        # Check that the "Saved Logins" window is empty.
        expected = exists(empty_saved_logins_pattern.similar(0.7), 10)
        assert expected, 'There are no logins saved.'

        # Close and check the "Saved Logins" window.
        type(Key.ESC)

        expected = exists(saved_logins_window_pattern, 10)
        assert expected is not True, '\"Saved Logins\" window is NOT displayed.'

        # Access the "Manage Data" window.
        expected = exists(manage_data_pattern, 10)
        assert expected, '\"Manage Data\" button has been found.'

        click(manage_data_pattern)

        # Check that "Manage Cookies and Site Data" window is displayed.
        expected = exists(manage_data_title_pattern, 10)
        assert expected, '\"Manage Cookies and Site Data\" window is displayed.'

        # Check that the "Manage Cookies and Site Data" window is empty.
        region = Screen().new_region(0, Screen.SCREEN_HEIGHT / 2 - 100, Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGHT/2)

        expected = region.exists('ago', 10)
        assert not expected, 'Cookies were deleted.'

        # Close and check the "Manage Cookies and Site Data" window.
        type(Key.ESC)

        expected = exists(manage_data_title_pattern, 10)
        assert expected is not True, '\"Manage Cookies and Site Data\" window is NOT displayed.'

        # Check that no disk space is used for cookies, site data and cache.
        expected = exists('using 0', 10)
        assert expected, 'No disk space is used to store cookies, site data and cache.'
