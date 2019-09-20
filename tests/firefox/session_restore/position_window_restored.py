# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Width, height and position of each window are restored.',
        test_case_id='114826',
        test_suite_id='68',
        locales=Locales.ENGLISH,
        preferences={'devtools.chrome.enabled': True},
        blocked_by={'id': 'issue_2925', 'platform': [OSPlatform.LINUX, OSPlatform.WINDOWS]},
    )
    def run(self, firefox):
        firefox_test_site_tab_pattern = Pattern('firefox_test_site_tab.png').similar(0.8)
        focus_test_site_tab_pattern = Pattern('focus_test_site_tab.png').similar(0.8)
        restore_previous_session_pattern = Pattern('restore_previous_session_item.png')
        console_output_500 = Pattern('console_output_height_500.png')
        console_output_height_400 = Pattern('console_output_height_400.png')
        console_output_width_1000 = Pattern('console_output_width_1000.png')
        browser_console_title_pattern = Pattern('browser_console_title.png')
        browser_console_empty_line_pattern = Pattern('browser_console_empty_line.png')

        if not OSHelper.is_mac():
            hamburger_menu_quit_item_pattern = Pattern('hamburger_menu_quit_item.png').similar(0.9)

        click_duration = 1
        drop_location = Location(100, 300)

        iris_tab_displayed = exists(LocalWeb.IRIS_LOGO_ACTIVE_TAB,
                                    region=Screen.TOP_THIRD)
        assert iris_tab_displayed, 'Iris tab is displayed properly'

        iris_tab_start_location = find(LocalWeb.IRIS_LOGO_ACTIVE_TAB)

        click(LocalWeb.IRIS_LOGO_ACTIVE_TAB, 1)
        time.sleep(FirefoxSettings.SHORT_FIREFOX_TIMEOUT)

        # - Drag some tags outside the main browser window.
        # - Position them in different places.
        # - Perform some changes to their height and width.
        open_browser_console()

        browser_console_opened = exists(browser_console_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_console_opened, 'Browser console opened.'

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        paste('window.resizeTo(1000, 400)')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        type(Key.ENTER)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        browser_console_empty_line = exists(browser_console_empty_line_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_console_empty_line, 'Value entered in browser console.'

        # prevent Linux to overlap windows
        click(iris_tab_start_location, 1)

        time.sleep(FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        open_browser_console()

        iris_tab_displayed = exists(LocalWeb.IRIS_LOGO_ACTIVE_TAB,
                                    region=Screen.TOP_THIRD)
        assert iris_tab_displayed, 'Iris tab is displayed properly'

        click(LocalWeb.IRIS_LOGO_ACTIVE_TAB, FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        time.sleep(FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        open_browser_console()

        browser_console_opened = exists(browser_console_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_console_opened, 'Browser console opened.'

        # deal with Linux error log first time blocks input
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        paste('window.resizeTo(1000, 400)')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        type(Key.ENTER)

        browser_console_empty_line = exists(browser_console_empty_line_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_console_empty_line, 'Value entered in browser console.'

        paste('window.moveTo(' + str(iris_tab_start_location.x) + ',' + str(iris_tab_start_location.y) + ')')
        type(Key.ENTER)

        close_tab()

        # open another websites and change their windows

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        tab_one_loaded = exists(firefox_test_site_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert tab_one_loaded, 'First tab loaded'

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)
        tab_two_loaded = exists(focus_test_site_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert tab_two_loaded, 'Second tab loaded'

        # drop second tab
        drag_drop(focus_test_site_tab_pattern, drop_location)
        time.sleep(FirefoxSettings.SHORT_FIREFOX_TIMEOUT)

        open_browser_console()

        browser_console_opened = exists(browser_console_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_console_opened, 'Browser console opened.'

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        paste('window.moveTo(0, ' + str(Screen.SCREEN_HEIGHT / 2 + 200) + ')')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        type(Key.ENTER)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        browser_console_empty_line = exists(browser_console_empty_line_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_console_empty_line, 'Value entered in browser console.'

        close_tab()

        # drop second tab

        firefox_tab = exists(firefox_test_site_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert firefox_tab, 'Firefox tab available.'

        drag_drop(firefox_test_site_tab_pattern, drop_location)
        time.sleep(FirefoxSettings.SHORT_FIREFOX_TIMEOUT)

        open_browser_console()

        browser_console_opened = exists(browser_console_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_console_opened, 'Browser console opened.'

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        paste('window.resizeTo(500, 500)')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        type(Key.ENTER)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        browser_console_empty_line = exists(browser_console_empty_line_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_console_empty_line, 'Value entered in browser console.'

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        paste('window.moveTo(' + str(Screen.SCREEN_WIDTH / 2) + ',' + str(Screen.SCREEN_HEIGHT / 15) + ')')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        type(Key.ENTER)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        browser_console_empty_line = exists(browser_console_empty_line_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_console_empty_line, 'Value entered in browser console.'

        close_tab()

        firefox.restart()

        # 4. Close Firefox from the "Hamburger" menu.
        # 5. Launch Firefox with the same profile.
        # 6. Open the "Hamburger" menu.
        # 7. Click the "Restore Previous session" button.
        # The previous session is successfully restored and the width,
        # height and position of each tab is displayed as
        # in the previous session.

        firefox_restarted = exists(NavBar.HAMBURGER_MENU.similar(0.9), FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert firefox_restarted, 'Firefox restarted successfully'

        click(NavBar.HAMBURGER_MENU, duration=click_duration)

        restore_previous_session_located = exists(restore_previous_session_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert restore_previous_session_located, \
            'The "Hamburger" menu is successfully displayed. "Restore previous session" menu item located'

        click(restore_previous_session_pattern, click_duration)

        time.sleep(FirefoxSettings.SHORT_FIREFOX_TIMEOUT)

        firefox_test_site_restored = exists(firefox_test_site_tab_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert firefox_test_site_restored, 'Firefox webpage is opened'

        firefox_tab_location = find(firefox_test_site_tab_pattern)

        # check first tab
        click(firefox_tab_location, click_duration)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        open_browser_console()

        browser_console_opened = exists(browser_console_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_console_opened, 'Browser console opened.'

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        paste('window.innerHeight')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        type(Key.ENTER)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        test_site_window_height_matched = exists(console_output_500, FirefoxSettings.FIREFOX_TIMEOUT)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        paste('window.innerWidth')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        type(Key.ENTER)

        test_site_window_width_matched = exists(console_output_500,
                                                FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_site_window_width_matched and test_site_window_height_matched, 'First window (Firefox) size matched'
        close_tab()

        # check second tab
        focus_tab_loaded = exists(focus_test_site_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert focus_tab_loaded, 'Focus tab loaded'

        focus_tab_location = find(focus_test_site_tab_pattern)

        click(focus_tab_location)

        open_browser_console()

        browser_console_opened = exists(browser_console_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_console_opened, 'Browser console opened.'

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        paste('window.innerHeight')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        type(Key.ENTER)

        focus_site_window_height_matched = exists(console_output_height_400, FirefoxSettings.FIREFOX_TIMEOUT)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        paste('window.innerWidth')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        type(Key.ENTER)
        focus_site_window_width_matched = exists(console_output_width_1000, FirefoxSettings.FIREFOX_TIMEOUT)
        assert focus_site_window_height_matched and focus_site_window_width_matched, \
            'Second window (Focus) size matched'

        close_tab()

        iris_tab_active = exists(LocalWeb.IRIS_LOGO_ACTIVE_TAB, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert iris_tab_active, 'Iris tab is active'

        iris_tab_location = find(LocalWeb.IRIS_LOGO_ACTIVE_TAB)

        click(iris_tab_location, 1)

        open_browser_console()

        browser_console_opened = exists(browser_console_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_console_opened, 'Browser console opened.'

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        paste('window.innerHeight')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        type(Key.ENTER)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        iris_window_height_matched = exists(console_output_height_400)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        paste('window.innerWidth')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        type(Key.ENTER)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        iris_window_width_matched = exists(console_output_width_1000)
        assert iris_window_height_matched and iris_window_width_matched, \
            'Iris window size matched.'

        # check positioning of windows after restart
        iris_tab_top = iris_tab_location.y < firefox_tab_location.y < focus_tab_location.y
        firefox_tab_right = iris_tab_location.x and focus_tab_location.x < firefox_tab_location.x
        assert iris_tab_top and firefox_tab_right, 'The previous session is successfully restored and ' \
                                                   'the width, height and position of each tab is displayed as ' \
                                                   'in the previous session.'