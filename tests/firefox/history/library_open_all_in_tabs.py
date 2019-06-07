# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open all the history from a history time range.',
        locale=['en-US'],
        test_case_id='174033',
        test_suite_id='2000'
    )
    def run(self, firefox):
        iris_tab_icon = Pattern('iris_logo_tab.png')
        mozilla_tab_icon = Pattern('mozilla_logo_tab.png')
        iris_bookmark_pattern = Pattern('iris_bookmark.png')
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        history_today_pattern = Library.HISTORY_TODAY
        new_tab_pattern = Pattern('new_tab.png')
        privacy_url = "http://www.mozilla.org/en-US/privacy/firefox/"
        firefox_privacy_logo_pattern = Pattern('firefox_privacy_logo_for_bookmarks.png')

        # Open a page to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected is True, 'Mozilla page loaded successfully.'

        new_tab()
        previous_tab()
        close_tab()

        navigate(privacy_url)
        new_tab()
        previous_tab()
        close_tab()

        # Open History and check if it is populated with the Iris page.
        open_library_menu('History')

        right_upper_corner = Screen().new_region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2,
                                                 Screen.SCREEN_HEIGHT / 2)

        expected = right_upper_corner.exists(iris_bookmark_pattern, 10)
        assert expected is True, 'Iris page is displayed in the History menu list.'

        click(show_all_history_pattern)

        expected = exists(history_today_pattern, 10)
        assert expected is True, 'Today history option is available.'

        # Right click on History time range and select the Open All in Tabs button.
        right_click(history_today_pattern)
        type(text='o')

        close_auxiliary_window = False
        if OSHelper.is_mac() or exists(Library.TITLE, 10):
            click_window_control('close')
            time.sleep(Settings.DEFAULT_UI_DELAY)
        else:
            close_auxiliary_window = True

        # Make sure that all the pages from the selected history time range are opened in the current window.
        expected = exists(iris_tab_icon, 10)
        assert expected is True, 'Iris local page loaded successfully.'

        expected = exists(mozilla_tab_icon, 10)
        assert expected is True, 'Mozilla page loaded successfully.'

        expected = exists(firefox_privacy_logo_pattern, 10)
        assert expected is True, 'Firefox Privacy Notice page loaded successfully.'

        expected = exists(new_tab_pattern, 10)
        assert expected is True, 'about:newtab page loaded successfully.'

        # Close potentially existing background library window
        if close_auxiliary_window:
            library_toolbar_icon = Pattern('library_icon.png')
            firefox_toolbar_icon = Pattern('firefox_icon.png')
            click(firefox_toolbar_icon)
            time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
            click(library_toolbar_icon)

            click_window_control('close')
            time.sleep(Settings.DEFAULT_UI_DELAY)

            click(firefox_privacy_logo_pattern)
