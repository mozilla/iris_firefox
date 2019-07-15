# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox can be se to use custom settings for history',
        test_case_id='143605',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        always_private_pattern = Pattern('always_private.png')
        remember_all_history_pattern = Pattern('remember_history.png')
        remember_browsing_history_pattern = Pattern('remember_browsing_download_history.png')
        clear_history_closing_pattern = Pattern('clear_history_when_closes.png')
        custom_history_settings_pattern = Pattern('custom_history_settings.png')
        remember_search_history_pattern = Pattern('remember_search_form_history.png')
        prefs_checked_box_pattern = Pattern('prefs_checked_box.png')
        prefs_unchecked_box_pattern = Pattern('prefs_unchecked_box.png')
        ui_timeout = 1

        box_width, box_heigth = prefs_checked_box_pattern.get_size()

        navigate('about:preferences#privacy')
        preferences_opened = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED)
        assert preferences_opened, 'Preferences page is opened'

        paste('Firefox will')
        history_preferences_reachable = exists(remember_all_history_pattern)
        assert history_preferences_reachable, 'History menu is reachable'

        click(remember_all_history_pattern)

        history_menu_opened = exists(custom_history_settings_pattern)
        assert history_menu_opened, 'History preferences menu is opened'

        click(custom_history_settings_pattern)

        custom_history_settings_opened = exists(always_private_pattern)
        assert custom_history_settings_opened, 'Custom history list is displayed'

        always_private_location = find(always_private_pattern)

        always_private_width, always_private_height = always_private_pattern.get_size()
        always_private_region = Region(always_private_location.x - box_width * 2, always_private_location.y,
                                       always_private_width, always_private_height)

        always_private_unchecked = exists(prefs_unchecked_box_pattern, region=always_private_region)
        assert always_private_unchecked, '"Always use private browsing mode" is off'

        remember_browsing_history_displayed = exists(remember_browsing_history_pattern)
        assert remember_browsing_history_displayed, '"Remember browsing history" point is displayed'

        remember_browsing_location = find(remember_browsing_history_pattern)
        remember_browsing_width, remember_browsing_height = remember_browsing_history_pattern.get_size()
        remember_browsing_region = Region(remember_browsing_location.x - box_width * 2, remember_browsing_location.y,
                                          remember_browsing_width, remember_browsing_height)

        remember_browsing_checked = exists(prefs_checked_box_pattern, region=remember_browsing_region)
        assert remember_browsing_checked, '"Remember browsing and download history" point is checked'

        remember_search_history_reachable = exists(remember_search_history_pattern)
        assert remember_search_history_reachable, '"Remember search and form history" point is displayed'

        remember_search_location = find(remember_search_history_pattern)
        remember_search_width, remember_search_height = remember_search_history_pattern.get_size()
        remember_search_region = Region(remember_search_location.x - box_width * 2, remember_search_location.y,
                                        remember_search_width, remember_search_height)

        remember_search_checked = exists(prefs_checked_box_pattern, region=remember_search_region)
        assert remember_search_checked, '"Remember search and forms history" point is checked'

        clear_history_closing_reachable = exists(clear_history_closing_pattern)
        assert clear_history_closing_reachable, '"Clear history when Firefox closed" point is displayed'

        clear_history_location = find(clear_history_closing_pattern)
        clear_history_width, clear_history_height = clear_history_closing_pattern.get_size()
        clear_history_region = Region(clear_history_location.x - box_width * 2, clear_history_location.y,
                                      clear_history_width, clear_history_height)

        remember_search_checked = exists(prefs_unchecked_box_pattern, region=clear_history_region)
        assert remember_search_checked, '"Clear history" point is unchecked'

        new_tab()
        new_tab_opened = exists(Tabs.NEW_TAB_HIGHLIGHTED)
        assert new_tab_opened, 'New tab is opened'

        navigate(LocalWeb.FIREFOX_TEST_SITE)
        firefox_page_loaded = exists(LocalWeb.FIREFOX_LOGO, Settings.site_load_timeout)
        assert firefox_page_loaded, 'Firefox local page is loaded'

        navigate(LocalWeb.FOCUS_TEST_SITE)
        focus_page_loaded = exists(LocalWeb.FOCUS_LOGO, Settings.site_load_timeout)
        assert focus_page_loaded, 'Focus local page is loaded'

        navigate(LocalWeb.POCKET_TEST_SITE)
        pocket_page_loaded = exists(LocalWeb.POCKET_IMAGE, Settings.site_load_timeout)
        assert pocket_page_loaded, 'Focus local page is loaded'

        select_tab(1)
        clear_history_closing_reachable = exists(clear_history_closing_pattern)
        assert clear_history_closing_reachable, '"Clear history when Firefox closed" point is displayed'

        click(clear_history_closing_pattern)

        firefox.restart()

        firefox_restarted = exists(NavBar.LIBRARY_MENU)
        assert firefox_restarted, 'Firefox is restarted'

        click(NavBar.LIBRARY_MENU)

        sidebar_menu_bar_opened = exists(Sidebar.HistorySidebar.SIDEBAR_HISTORY_ICON)
        assert sidebar_menu_bar_opened, 'Sidebar is opened'

        click(Sidebar.HistorySidebar.SIDEBAR_HISTORY_ICON)

        history_submenu_opened = exists(History.HistoryMenu.VIEW_HISTORY_SIDEBAR)
        assert history_submenu_opened, 'History submenu is opened'

        firefox_page_not_visited = not exists(LocalWeb.FIREFOX_BOOKMARK.similar(0.9), ui_timeout)
        assert firefox_page_not_visited, 'Firefox local page visit was\'nt saved in history'

        focus_page_not_visited = not exists(LocalWeb.FOCUS_BOOKMARK.similar(0.9), ui_timeout)
        assert focus_page_not_visited, 'Focus local page visit was\'nt saved in history'

        pocket_page_not_visited = not exists(LocalWeb.POCKET_BOOKMARK.similar(0.9), ui_timeout)
        assert pocket_page_not_visited, 'Pocket local page visit was\'nt saved in history'

        restore_firefox_focus()
