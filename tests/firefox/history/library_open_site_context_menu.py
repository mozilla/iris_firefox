# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Use Open button from the contextual options.',
        locale=['en-US'],
        test_case_id='174038',
        test_suite_id='2000',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        history_today_pattern = Library.LIBRARY_WINDOW_HISTORY_TODAY
        mozilla_bookmark_history_list_pattern = LocalWeb.MOZILLA_BOOKMARK_LIBRARY_HISTORY_LIST
        iris_logo_tab_pattern = Pattern('iris_logo_tab.png')
        iris_bookmark_pattern = Pattern('iris_bookmark.png')

        # Open a page to create some today's history.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected_1 = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected_1 is True, 'Mozilla page loaded successfully.'

        close_tab()

        # Select the History option from the View History, saved bookmarks and more Menu.
        open_library_menu('History')
        right_upper_corner = Screen().new_region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2,
                                                 Screen.SCREEN_HEIGHT / 2)

        expected_2 = right_upper_corner.exists(iris_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected_2 is True, 'Iris page is displayed in the History menu list.'

        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)

        # Click on the Show All History button.
        click(show_all_history_pattern, 1)

        expected_3 = exists(history_today_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected_3 is True, 'Today history option is available.'

        type(Key.DOWN)

        expected_4 = exists(mozilla_bookmark_history_list_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected_4 is True, 'Mozilla page is displayed successfully in the History list.'

        # Open the Mozilla page using the 'Open' button from the context menu.
        right_click(mozilla_bookmark_history_list_pattern)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)
        type(text='o')

        # Close the library.
        open_library()
        click_window_control('close')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)

        # Check that the Mozilla page loaded successfully in the current tab(Iris page).
        expected_5 = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected_5 is True, 'Mozilla page loaded successfully.'

        expected_6 = exists(iris_logo_tab_pattern, 3)
        assert expected_6 is False, 'Mozilla page loaded successfully in the current tab.'
