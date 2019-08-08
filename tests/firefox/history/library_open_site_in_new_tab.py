# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Use \'Open in a New Tab\' button from the contextual options.',
        locale=['en-US'],
        test_case_id='174039',
        test_suite_id='2000',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        iris_bookmark_pattern = Pattern('iris_bookmark.png')
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        history_today_pattern = Library.LIBRARY_WINDOW_HISTORY_TODAY
        mozilla_bookmark_history_pattern = LocalWeb.MOZILLA_BOOKMARK_LIBRARY_HISTORY_LIST
        iris_tab_icon = Pattern('iris_logo_tab.png')

        # Open a page to create some today's history.
        new_tab()

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        test_site_opened = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_site_opened is True, 'Mozilla page loaded successfully.'

        close_tab()

        # Select the History option from the View History, saved bookmarks and more Menu.
        open_library_menu('History')

        right_upper_corner = Screen().new_region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2,
                                                 Screen.SCREEN_HEIGHT / 2)

        iris_displayed_in_history = right_upper_corner.exists(iris_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert iris_displayed_in_history is True, 'Iris page is displayed in the History menu list.'

        # Click on the Show All History button.
        click(show_all_history_pattern, 2)

        today_option_exists = exists(history_today_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert today_option_exists is True, 'Today history option is available.'

        type(Key.DOWN)

        # Verify if Mozilla page is present in Today's History.

        mozilla_displayed_in_history = exists(mozilla_bookmark_history_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_displayed_in_history is True, 'Mozilla page is displayed successfully in the History list.'

        # Open the Mozilla page using the 'Open in a New Tab' button from the context menu.
        right_click(mozilla_bookmark_history_pattern)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)

        type(text='w')

        # Close the library.
        open_library()

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)

        click_window_control('close')

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)

        # Check that the Mozilla page loaded successfully in a new tab.
        test_site_opened = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_site_opened is True, 'Mozilla page loaded successfully.'

        iris_page_displayed = exists(iris_tab_icon, FirefoxSettings.FIREFOX_TIMEOUT)
        assert iris_page_displayed is True, 'Iris local page is still open in the first tab.'
