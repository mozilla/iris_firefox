# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description=' History can be cleared via the "Clear Recent History" panel ',
        test_case_id='143611',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        clear_everything_history_pattern = Pattern('clear_everything_history.png')
        clear_history_button_pattern = Pattern('clear_history_button.png')
        clear_history_today_pattern = Pattern('clear_history_today.png')
        clear_last_four_hours_history_pattern = Pattern('clear_last_four_hours_history.png')
        clear_last_hour_history_pattern = Pattern('clear_last_hour_history.png')
        clear_last_two_hours_history_pattern = Pattern('clear_last_two_hours_history.png')
        clear_now_button_pattern = Pattern('clear_now_button.png')
        ui_timeout = 1

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        firefox_page_loaded = exists(LocalWeb.FIREFOX_LOGO, Settings.site_load_timeout)
        assert firefox_page_loaded, 'Firefox local page is loaded'

        navigate(LocalWeb.FOCUS_TEST_SITE)
        focus_page_loaded = exists(LocalWeb.FOCUS_LOGO)
        assert focus_page_loaded, 'Focus local page is loaded'

        close_tab()

        navigation_bar_reachable = exists(NavBar.LIBRARY_MENU)
        assert navigation_bar_reachable, 'Navigation bar reachable'

        click(NavBar.LIBRARY_MENU)

        sidebar_menu_bar_opened = exists(Sidebar.HistorySidebar.SIDEBAR_HISTORY_ICON)
        assert sidebar_menu_bar_opened, 'Sidebar is opened'

        click(Sidebar.HistorySidebar.SIDEBAR_HISTORY_ICON)

        history_submenu_opened = exists(History.HistoryMenu.VIEW_HISTORY_SIDEBAR)
        assert history_submenu_opened, 'History submenu is opened'

        firefox_page_visited = exists(LocalWeb.FIREFOX_BOOKMARK)
        assert firefox_page_visited, 'Firefox local page visit was saved in history'

        focus_page_visited = exists(LocalWeb.FOCUS_BOOKMARK)
        assert focus_page_visited, 'Focus local page visit was saved in history'

        restore_firefox_focus()

        navigate('about:preferences#privacy')
        preferences_privacy_opened = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED)
        assert preferences_privacy_opened, 'The about:preferences page is successfully loaded.The options for ' \
                                           '"Privacy & Security" section are displayed.'

        paste('Firefox will')
        history_prefs_displayed = exists(clear_history_button_pattern)
        assert history_prefs_displayed, 'History section in privacy preferences is displayed'

        click(clear_history_button_pattern)

        history_purging_settings_opened = exists(clear_last_hour_history_pattern)
        assert history_purging_settings_opened, '"Clear recent history" sub-window is opened'

        click(clear_last_hour_history_pattern)

        clear_last_two_hours_history_displayed = exists(clear_last_two_hours_history_pattern)
        assert clear_last_two_hours_history_displayed, 'Time range menu is displayed properly'

        clear_last_four_hours_history_displayed = exists(clear_last_four_hours_history_pattern)
        assert clear_last_four_hours_history_displayed, 'Time range menu is displayed properly'

        clear_history_today_displayed = exists(clear_history_today_pattern)
        assert clear_history_today_displayed, 'Time range menu is displayed properly'

        clear_everything_history_displayed = exists(clear_everything_history_pattern)
        assert clear_everything_history_displayed, 'Time range menu is displayed properly'

        click(clear_history_today_pattern)

        sub_window_displayed=exists(clear_now_button_pattern)
        assert sub_window_displayed, 'Sub-window is still displayed'

        click(clear_now_button_pattern)

        navigation_bar_reachable = exists(NavBar.LIBRARY_MENU)
        assert navigation_bar_reachable, 'Navigation bar reachable'

        click(NavBar.LIBRARY_MENU)

        sidebar_menu_bar_opened = exists(Sidebar.HistorySidebar.SIDEBAR_HISTORY_ICON)
        assert sidebar_menu_bar_opened, 'Sidebar is opened'

        click(Sidebar.HistorySidebar.SIDEBAR_HISTORY_ICON)

        history_submenu_opened = exists(History.HistoryMenu.VIEW_HISTORY_SIDEBAR)
        assert history_submenu_opened, 'History submenu is opened'

        firefox_page_visit_deleted = not exists(LocalWeb.FIREFOX_BOOKMARK, ui_timeout)
        assert firefox_page_visit_deleted, 'Firefox local page visit was deleted from history'

        focus_page_visit_deleted = not exists(LocalWeb.FOCUS_BOOKMARK, ui_timeout)
        assert focus_page_visit_deleted, 'Focus local page visit was deleted from history'
