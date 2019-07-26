# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox can be successfully set to never remember history',
        locale=['en-US'],
        test_case_id='143604',
        test_suite_id='2241',
    )
    def run(self, firefox):
        remember_history_selected_pattern = Pattern('remember_history_selected.png')
        never_remember_history_pattern = Pattern('never_remember_history.png')
        restart_browser_pattern = Pattern('restart_browser.png')
        ui_timeout = 1

        navigate('about:preferences#privacy')

        preferences_opened = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED)
        assert preferences_opened, 'Preferences page is successfully displayed on privacy block'

        paste('firefox will')
        remember_history_menu_found = exists(remember_history_selected_pattern)
        assert remember_history_menu_found, 'History menu found, Firefox already set to remember history'

        click(remember_history_selected_pattern)

        history_settings_menu_opened = exists(never_remember_history_pattern)
        assert history_settings_menu_opened, 'History settings menu is opened'

        click(never_remember_history_pattern)

        restart_browser_opened = exists(restart_browser_pattern)
        assert restart_browser_opened, 'restart_browser_pattern'

        click(restart_browser_pattern)

        browser_relaunched = exists(NavBar.LIBRARY_MENU, Settings.site_load_timeout) and exists(
            NavBar.SIDEBAR_MENU, Settings.site_load_timeout)
        assert browser_relaunched, 'Browser is relaunched'

        navigate(LocalWeb.FIREFOX_TEST_SITE)
        firefox_site_loaded = exists(LocalWeb.FIREFOX_LOGO, Settings.site_load_timeout)
        assert firefox_site_loaded, 'Firefox local web page is loaded'

        navigate(LocalWeb.FOCUS_TEST_SITE)
        focus_site_loaded = exists(LocalWeb.FOCUS_IMAGE, Settings.site_load_timeout)
        assert focus_site_loaded, 'Focus local web page is loaded'

        navigate(LocalWeb.POCKET_TEST_SITE)
        iris_page_loaded = exists(LocalWeb.POCKET_IMAGE, Settings.site_load_timeout)
        assert iris_page_loaded, 'Iris local page is loaded'

        library_menu_button_reachable = exists(NavBar.LIBRARY_MENU)
        assert library_menu_button_reachable, 'Library menu button is reachable'

        click(NavBar.LIBRARY_MENU)

        history_block_reachable = exists(LibraryMenu.HISTORY_BUTTON)
        assert history_block_reachable, 'History block is reachable'

        click(LibraryMenu.HISTORY_BUTTON)

        hist = exists(History.HistoryMenu.VIEW_HISTORY_SIDEBAR)
        assert hist, 'History submenu is opened'

        firefox_page_visited = not exists(LocalWeb.FIREFOX_BOOKMARK.similar(0.9), ui_timeout)
        assert firefox_page_visited, 'Firefox local page visit was saved in history'

        focus_page_visited = not exists(LocalWeb.FOCUS_BOOKMARK.similar(0.9), ui_timeout)
        assert focus_page_visited, 'Focus local page visit was saved in history'

        pocket_page_visited = not exists(LocalWeb.POCKET_BOOKMARK.similar(0.9), ui_timeout)
        assert pocket_page_visited, 'Pocket local page visit was saved in history'

        restore_firefox_focus()
